from __future__ import division


import numpy as np


import pylab as plt
from solvers.grid_functions import fastgather


class UniformGrid(object):
    '''
    classdocs
    '''

    def __init__(self, extension_x, extension_y, nx, ny):

        self.n_macroparticles = nx * ny

        self.id = np.arange(1, nx * ny + 1)

        self.nx, self.ny = nx, ny

        self.rho = np.zeros((ny, nx))

        self.dx = 2 * extension_x / (nx - 1)
        self.dy = 2 * extension_y / (ny - 1)

        mx = np.arange(-extension_x, extension_x + self.dx, self.dx)
        my = np.arange(-extension_y, extension_y + self.dy, self.dy)

        self.x, self.y = np.meshgrid(mx, my)

        from types import MethodType
        UniformGrid.fastgather = MethodType(fastgather, None, UniformGrid)

    def gather(self, bunch, i_slice):

        '''
        Cell
        3 ------------ 4
        |     |        |
        |     |        |
        |     |        |
        |     |        |
        |-----x--------|
        |     |        |
        1 ------------ 2
        '''

        # Initialise
        self.rho[:] = 0

        # On regular mesh
        dx = self.x[0, 1] - self.x[0, 0]
        dy = self.y[1, 0] - self.y[0, 0]
        dxi = 1 / dx
        dyi = 1 / dy
        ai = 1 / (dx * dy)
        # TODO: on adaptive mesh

        # Line charge density and particle selection
        # double lambda;
        # std::vector<int> index;
        # t.get_slice(i_slice, lambda, index);
        # int np = index.size();
        l = 1
        x, y = bunch.x, bunch.y

        fx, fy = (x - self.x[0,0]) * dxi, (y - self.y[0,0]) * dyi
        ix, iy = np.floor(fx).astype(int), np.floor(fy).astype(int)
        fx, fy = fx - ix, fy - iy

        H, xedges, yedges = np.histogram2d(ix, iy, bins=self.rho.shape)
        self.rho += H

    @profile
    def track(self, bunch):

        fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)

        for i in xrange(bunch.slices.n_slices):
            self.gather(bunch, i)
        ax1.contourf(self.x, self.y, self.rho, 100)
        ax1.scatter(bunch.x, bunch.y, c='y', marker='.', alpha=0.1, lw=0)
        ax1.set_aspect('equal')

        for i in xrange(bunch.slices.n_slices):
            self.fastgather(bunch.x, bunch.y)
        ax2.contourf(self.x, self.y, self.rho, 100)
        ax2.scatter(bunch.x, bunch.y, c='y', marker='.', alpha=0.1, lw=0)
        ax2.set_aspect('equal')

        plt.show()

# template<typename T, typename U>
# void PoissonBase::fastscatter(T t, U u, int i_slice)
# {
#     int np;
#     double qp;
#     std::vector<int> ip;

#     /*
#      * Cell
#      *
#      *  3 ------------ 4
#      *  |     |        |
#      *  |     |        |
#      *  |     |        |
#      *  |     |        |
#      *  |-----x--------|
#      *  |     |        |
#      *  1 ------------ 2
#      */

#     // On regular mesh
#     const double dx = (mx.back() - mx.front()) / (n_points_x - 1);
#     const double dy = (my.back() - my.front()) / (n_points_y - 1);
#     const double dxi = 1 / dx;
#     const double dyi = 1 / dy;
#     // TODO: on adaptive mesh

#     // Line charge density and particle selection
#     t.get_slice(i_slice, np, qp, ip);

#     // t impacting fields
#     for (int j=0; j<np; j++)
#     {
#       double xp = t.x[ip[j]];
#       double yp = t.y[ip[j]];

#       // Compute points
#       double fx = (xp - mx[0]) * dxi;
#       double fy = (yp - my[0]) * dyi;
#       int ix = std::floor(fx);
#       int iy = std::floor(fy);

#       size_t k1 = iy * n_points_x + ix;
#       size_t k2 = iy * n_points_x + ix + 1;
#       size_t k3 = (iy + 1) * n_points_x + ix;
#       size_t k4 = (iy + 1) * n_points_x + ix + 1;

#       // Compute normalized area
#       fx -= ix;
#       fy -= iy;

#       double a1 = (1 - fx) * (1 - fy);
#       double a2 = fx * (1 - fy);
#       double a3 = (1 - fx) * fy;
#       double a4 = fx * fy;

#       // Scatter fields
#       t.kx[ip[j]] = (u.ex_g[k1] * a1 + u.ex_g[k2] * a2
#                      + u.ex_g[k3] * a3 + u.ex_g[k4] * a4);
#       t.ky[ip[j]] = (u.ey_g[k1] * a1 + u.ey_g[k2] * a2
#                      + u.ey_g[k3] * a3 + u.ey_g[k4] * a4);
#     }

#     // Line charge density and particle selection
#     u.get_slice(i_slice, np, qp, ip);

#     // u impacting fields
#     for (int j=0; j<np; j++)
#     {
#       double xp = u.x[ip[j]];
#       double yp = u.y[ip[j]];

#       // Compute points
#       double fx = (xp - mx[0]) * dxi;
#       double fy = (yp - my[0]) * dyi;
#       int ix = std::floor(fx);
#       int iy = std::floor(fy);

#       size_t k1 = iy * n_points_x + ix;
#       size_t k2 = iy * n_points_x + ix + 1;
#       size_t k3 = (iy + 1) * n_points_x + ix;
#       size_t k4 = (iy + 1) * n_points_x + ix + 1;

#       // Compute normalized area
#       fx -= ix;
#       fy -= iy;

#       double a1 = (1 - fx) * (1 - fy);
#       double a2 = fx * (1 - fy);
#       double a3 = (1 - fx) * fy;
#       double a4 = fx * fy;

#       // Scatter fields
#       u.kx[ip[j]] = (t.ex_g[k1] * a1 + t.ex_g[k2] * a2
#                      + t.ex_g[k3] * a3 + t.ex_g[k4] * a4);
#       u.ky[ip[j]] = (t.ey_g[k1] * a1 + t.ey_g[k2] * a2
#                      + t.ey_g[k3] * a3 + t.ey_g[k4] * a4);
#     }
# }

# template<typename T, typename U>
# void PoissonBase::parallelscatter(T t, U u, int i_slice)
# {
#     /*
#      * Cell
#      *
#      *  3 ------------ 4
#      *  |     |        |
#      *  |     |        |
#      *  |     |        |
#      *  |     |        |
#      *  |-----x--------|
#      *  |     |        |
#      *  1 ------------ 2
#      */

#     // On regular mesh
#     const double dx = (mx.back() - mx.front()) / (n_points_x - 1);
#     const double dy = (my.back() - my.front()) / (n_points_y - 1);
#     const double dxi = 1 / dx;
#     const double dyi = 1 / dy;
#     const double mx0 = mx[0];
#     const double my0 = my[0];
#     // TODO: on adaptive mesh

# //    // Separate variable for parallel processing
# //	// Line charge density and particle selection
# //	t.get_slice(i_slice, np, qp, ip);
# //
# //    std::vector<double> t_x(np);
# //    std::vector<double> t_y(np);
# //    std::vector<double> t_kx(np);
# //    std::vector<double> t_ky(np);
# //    std::vector<double> u_ex_g(n_points);
# //    std::vector<double> u_ey_g(n_points);
# //
# //    for (int j=0; j<np; j++)
# //    {
# //        t_x[j] = t.x[ip[j]];
# //        t_y[j] = t.y[ip[j]];
# ////      t_kx[j] = t.kx[ip[j]];
# ////      t_ky[j] = t.ky[ip[j]];
# //    }
# //
# //    for (size_t k=0; k<n_points; k++)
# //    {
# //        u_ex_g[k] = u.ex_g[k];
# //        u_ey_g[k] = u.ey_g[k];
# //    }
# //
# //    // Line charge density and particle selection
# //    u.get_slice(i_slice, np, qp, ip);
# //
# //    std::vector<double> u_x(np);
# //    std::vector<double> u_y(np);
# //    std::vector<double> u_kx(np);
# //    std::vector<double> u_ky(np);
# //    std::vector<double> t_ex_g(n_points);
# //    std::vector<double> t_ey_g(n_points);
# //
# //    for (int j=0; j<np; j++)
# //    {
# //        u_x[j] = u.x[ip[j]];
# //        u_y[j] = u.y[ip[j]];
# ////      u_kx[j] = u.kx[ip[j]];
# ////      u_ky[j] = u.ky[ip[j]];
# //    }
# //
# //    for (size_t k=0; k<n_points; k++)
# //    {
# //        t_ex_g[k] = t.ex_g[k];
# //        t_ey_g[k] = t.ey_g[k];
# //    }

# //#pragma omp parallel
# //{
# //#pragma omp sections nowait private(np, qp, ip)
# //{
# //#pragma omp section
# //{
#     int np;
#     double lambda;
#     std::vector<int> index;

#   // Line charge density and particle selection
#   t.get_slice(i_slice, lambda, index);
#   np = index.size();

#     // t impacting fields
#     for (int j=0; j<np; j++)
#     {
#         double xp = t.x[index[j]];
#         double yp = t.y[index[j]];

#         // Compute points
#         double fx = (xp - mx[0]) * dxi;
#         double fy = (yp - my[0]) * dyi;
#         int ix = std::floor(fx);
#         int iy = std::floor(fy);

#         size_t k1 = iy * n_points_x + ix;
#         size_t k2 = iy * n_points_x + ix + 1;
#         size_t k3 = (iy + 1) * n_points_x + ix;
#         size_t k4 = (iy + 1) * n_points_x + ix + 1;

#         // Compute normalized area
#         fx -= ix;
#         fy -= iy;

#         double a1 = (1 - fx) * (1 - fy);
#         double a2 = fx * (1 - fy);
#         double a3 = (1 - fx) * fy;
#         double a4 = fx * fy;

#         // Scatter fields
#         t.kx[index[j]] = (u.ex_g[k1] * a1 + u.ex_g[k2] * a2
#                      + u.ex_g[k3] * a3 + u.ex_g[k4] * a4);
#         t.ky[index[j]] = (u.ey_g[k1] * a1 + u.ey_g[k2] * a2
#                      + u.ey_g[k3] * a3 + u.ey_g[k4] * a4);
#     }
# //}
# //
# //#pragma omp section
# //{
#   // Line charge density and particle selection
#     u.get_slice(i_slice, lambda, index);
#     np = index.size();

#     // u impacting fields
#     for (int j=0; j<np; j++)
#     {
#         double xp = u.x[index[j]];
#         double yp = u.y[index[j]];

#         // Compute points
#         double fx = (xp - mx[0]) * dxi;
#         double fy = (yp - my[0]) * dyi;
#         int ix = std::floor(fx);
#         int iy = std::floor(fy);

#         size_t k1 = iy * n_points_x + ix;
#         size_t k2 = iy * n_points_x + ix + 1;
#         size_t k3 = (iy + 1) * n_points_x + ix;
#         size_t k4 = (iy + 1) * n_points_x + ix + 1;

#         // Compute normalized area
#         fx -= ix;
#         fy -= iy;

#         double a1 = (1 - fx) * (1 - fy);
#         double a2 = fx * (1 - fy);
#         double a3 = (1 - fx) * fy;
#         double a4 = fx * fy;

#         // Scatter fields
#         u.kx[index[j]] = (t.ex_g[k1] * a1 + t.ex_g[k2] * a2
#                      + t.ex_g[k3] * a3 + t.ex_g[k4] * a4);
#         u.ky[index[j]] = (t.ey_g[k1] * a1 + t.ey_g[k2] * a2
#                      + t.ey_g[k3] * a3 + t.ey_g[k4] * a4);
#     }
# //}
# //}
# //}
# }



class AdaptiveGrid(object):
    '''
    classdocs
    '''

    def __init__(self, extension_x, extension_y, nx, ny):
        '''
        l = sum_{k=1}^n dx_k
        dx_k = m * k
        => l = m * sum_{k=1}^n k = m * (n * (n + 1) / 2); m = 2 * l / (n * (n + 1))
        '''
        nx, ny = nx // 2, ny // 2
        mx = 2 * extension_x / (nx * (nx + 1))
        my = 2 * extension_y / (ny * (ny + 1))
        # dxk = np.arange(1, nx + 1) * mx
        # dyk = np.arange(1, ny + 1) * my
        lx, ly = np.zeros(nx), np.zeros(ny)
        lx[0], ly[0] = mx, my
        for i in xrange(1, nx):
            lx[i] = lx[i - 1] + mx * (i + 1)
        for i in xrange(1, ny):
            ly[i] = ly[i - 1] + my * (i + 1)

        self.mx = np.hstack((-lx[::-1], lx))
        self.my = np.hstack((-ly[::-1], ly))
