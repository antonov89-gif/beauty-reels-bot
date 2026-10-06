"""Real 3D terrain camera: satellite texture draped on an exaggerated DEM, rendered by per-pixel ray marching
(perspective, tilt, yaw, occlusion). World units: x = lon, y = mercator Y (deg), z = height (deg-equivalent)."""
import math

import cv2
import numpy as np

W, H = 1080, 1920
FOV_V = 40.0
F_PX = (H / 2) / math.tan(math.radians(FOV_V / 2))
EXAG = 14.0
M_PER_UNIT = 111320.0


def my(lat):
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


ELEV_CFG = ("elev_mid.npy", 4.0, 36.0, 120)
_EL = None


def elev():
    global _EL
    if _EL is None:
        _EL = np.minimum(np.load(ELEV_CFG[0]), 3500.0).astype(np.float32) * EXAG / M_PER_UNIT
    return _EL


def height_at(x, Y):
    E = elev()
    _, lon0, top, ppd = ELEV_CFG
    c = ((x - lon0) * ppd).astype(np.int32)
    r = ((my(top) - Y) * ppd).astype(np.int32)
    ok = (c >= 0) & (c < E.shape[1]) & (r >= 0) & (r < E.shape[0])
    out = np.zeros(np.shape(x), np.float32)
    out[ok] = E[r[ok], c[ok]]
    return out


class Cam3D:
    def __init__(self, lon, lat, span, tilt=20.0, yaw=0.0):
        self.span = span
        th, ps = math.radians(tilt), math.radians(yaw)
        hdir = np.array([math.sin(ps), math.cos(ps), 0.0])
        self.F = np.array([math.sin(th) * hdir[0], math.sin(th) * hdir[1], -math.cos(th)])
        self.R = np.array([math.cos(ps), -math.sin(ps), 0.0])
        self.U = np.cross(self.R, self.F)
        self.dist = span / 2 / ((W / 2) / F_PX)
        T = np.array([lon, my(lat), 0.0])
        self.C = T - self.dist * self.F
        self.ppd = W / span  # nominal, used for sizing only

    # ---------------- projection for overlays
    def proj(self, x, Y, z):
        v = np.stack([x - self.C[0], Y - self.C[1], z - self.C[2]], -1)
        xc, yc, zc = v @ self.R, v @ self.U, v @ self.F
        zc = np.where(zc > 1e-3, zc, np.nan)
        px = W / 2 + F_PX * xc / zc
        py = H / 2 - F_PX * yc / zc
        return np.nan_to_num(px, nan=-1e5), np.nan_to_num(py, nan=-1e5)

    def xy(self, lon, lat):
        Y = np.array([my(lat)])
        x = np.array([lon], np.float64)
        px, py = self.proj(x, Y, height_at(x, Y))
        return float(px[0]), float(py[0])

    def xyY(self, arr):
        x, Y = arr[:, 0], arr[:, 1]
        px, py = self.proj(x, Y, height_at(x, Y))
        return np.stack([px, py], 1)

    # ---------------- terrain render
    def ground(self, step=2, n=44):
        hw, hh = W // step, H // step
        a = ((np.arange(hw) + 0.5) * step - W / 2) / F_PX
        b = (H / 2 - (np.arange(hh) + 0.5) * step) / F_PX
        A, B = np.meshgrid(a.astype(np.float32), b.astype(np.float32))
        d = [self.F[k] + A * self.R[k] + B * self.U[k] for k in range(3)]
        zmax = float(elev().max())
        dz = np.minimum(d[2], -1e-4)
        t_top = np.maximum((zmax - self.C[2]) / dz, 0)
        t_bot = (0.0 - self.C[2]) / dz
        t_hit = t_bot.copy()
        hit = np.zeros(A.shape, bool)
        prev_t, prev_diff = t_top, None
        for k in range(n + 1):
            t = t_top + (t_bot - t_top) * (k / n)
            x = self.C[0] + d[0] * t
            Y = self.C[1] + d[1] * t
            diff = (self.C[2] + d[2] * t) - height_at(x, Y)
            if prev_diff is not None:
                new = (~hit) & (diff <= 0)
                if new.any():
                    fr = prev_diff[new] / np.maximum(prev_diff[new] - diff[new], 1e-9)
                    t_hit[new] = prev_t[new] + fr * (t[new] - prev_t[new])
                    hit |= new
            prev_t, prev_diff = t, diff
        gx = (self.C[0] + d[0] * t_hit).astype(np.float32)
        gY = (self.C[1] + d[1] * t_hit).astype(np.float32)
        gx = cv2.resize(gx, (W, H), interpolation=cv2.INTER_LINEAR)
        gY = cv2.resize(gY, (W, H), interpolation=cv2.INTER_LINEAR)
        tt = cv2.resize(t_hit.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR)
        return gx, gY, tt


def sample(arr, lon0, top_lat, ppd, gx, gY, fill):
    """cv2.remap from a (possibly memmapped) georeferenced array, cropping only the needed window."""
    u = (gx - lon0) * ppd
    v = (my(top_lat) - gY) * ppd
    u0, u1 = int(max(0, np.floor(u.min()) - 2)), int(min(arr.shape[1], np.ceil(u.max()) + 3))
    v0, v1 = int(max(0, np.floor(v.min()) - 2)), int(min(arr.shape[0], np.ceil(v.max()) + 3))
    if u1 <= u0 + 1 or v1 <= v0 + 1:
        return None
    crop = np.ascontiguousarray(arr[v0:v1, u0:u1])
    return cv2.remap(crop, (u - u0).astype(np.float32), (v - v0).astype(np.float32), cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=fill)
