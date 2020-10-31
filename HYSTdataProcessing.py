import numpy as np


class HYSTdata:

    def __init__(self, filename, dispcol, forcecol, delimiter, skiprows):
        """
        :param filename: name of the file to be read
        :param skiprows: rows that should be skipped
        """

        self.filename = filename
        self.disp = list(np.loadtxt('%s' % filename, delimiter=delimiter, usecols=(dispcol,), skiprows=skiprows, dtype=float))
        self.force = list(np.loadtxt('%s' % filename, delimiter=delimiter, usecols=(forcecol,), skiprows=skiprows, dtype=float))

    @staticmethod
    def energy(disp, force):
        """
        :param disp: 
        :param force: 
        :return: energy dissipated in [disp,force]
        """""
        energy = 0
        for i in range(1, len(disp)):
            l1 = force[i - 1]
            l2 = force[i]
            h = disp[i] - disp[i - 1]
            S = 0.5 * h * (l1 + l2)
            energy += S
        return energy

    @staticmethod
    def pointindex(searchpoint, searchlist, begin, end, slope):
        """
        :param searchpoint:
        :param searchlist:
        :param begin:
        :param end:
        :param slope: Slope>0: search in the increasing part; slope<0: search in the decreasing part
        :return: first index of searchpoint in searchlist[begin:end]
        """
        pointindex = 'NA'
        if slope > 0:
            for i in range(begin, end):
                if searchlist[i - 1] < searchpoint <= searchlist[i]:
                    pointindex = i
                    break
        if slope < 0:
            for i in range(begin, end):
                if searchlist[i - 1] > searchpoint >= searchlist[i]:
                    pointindex = i
                    break
        return pointindex

    # @property
    # def Ke(self):
    #     # Function: return intial stiffness of the curve
    #     force_p4 = 0.4 * self.maxforce
    #     Index_U4 = self.SearchPoint(force_p4, self.force, 0, len(self.force), 1)
    #     force_U4 = self.force[Index_U4]
    #     disp_U4 = self.disp[Index_U4]
    #     self.true_Ke = force_U4 / disp_U4
    #     return self.true_Ke
    #
    # @property
    # def Index_US(self):
    #     # Function: return index of the ultimate state
    #     Index_maxforce = self.SearchPoint(self.maxforce, self.force, 0, len(self.force), 1)
    #     force_maxforce = self.force[Index_maxforce]
    #     disp_maxforce = self.disp[Index_maxforce]
    #     force_p8 = 0.8 * self.maxforce
    #     self.true_Index_US = self.SearchPoint(force_p8, self.force, Index_maxforce, len(self.force), -1)
    #     if self.true_Index_US == 'NA':
    #         print('Can not find the point corresponding to ultimate state')
    #     return self.true_Index_US
    #
    # @property
    # def UltimatePoint(self):
    #     # Function: return [disp,force] of ultimate state
    #     if self.Index_US == 'NA':
    #         self.true_UltimatePoint = ['NA', 'NA']
    #     else:
    #         self.true_UltimatePoint = [self.disp[self.Index_US], self.force[self.Index_US]]
    #     return self.true_UltimatePoint
    #
    # @property
    # def UltimateEnergy(self):
    #     # Function: return energy dissipated in [0,ultimate state]
    #     if self.Index_US == 'NA':
    #         self.true_UltimateEnergy = 'NA'
    #     else:
    #         self.true_UltimateEnergy = self.CycleEnergy(self.disp[0:self.Index_US], self.force[0:self.Index_US])
    #     return self.true_UltimateEnergy
    #
    # @property
    # def YieldPoint(self):
    #     # Function: return [disp,force] of yield point
    #     if self.Index_US == 'NA':
    #         self.true_YieldPoint = ['NA', 'NA']
    #     else:
    #         flag = self.UltimatePoint[0] ** 2 - 2 * self.UltimateEnergy / self.Ke
    #         if flag < 0:
    #             self.true_YieldPoint = ['NA', 'NA']
    #         else:
    #             YieldForce = (self.UltimatePoint[0] - flag ** 0.5) * self.Ke
    #             YieldDisp = YieldForce / self.Ke
    #             self.true_YieldPoint = [YieldDisp, YieldForce]
    #     return self.true_YieldPoint
    #
    # @property
    # def Ductility(self):
    #     # Function: return ductility ratio
    #     if self.YieldPoint == ['NA', 'NA']:
    #         self.true_Ductility = 'NA'
    #     else:
    #         self.true_Ductility = self.UltimatePoint[0] / self.YieldPoint[0]
    #     return self.true_Ductility