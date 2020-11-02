import numpy as np


class HYSTdata:

    def __init__(self, filename, dispcol, forcecol, delimiter, skiprows):
        """
        :param filename: name of the file to be read
        :param skiprows: rows that should be skipped
        """

        self.filename = filename
        self.disp = list(np.loadtxt(filename, delimiter=delimiter, usecols=(dispcol,), skiprows=skiprows, dtype=float))
        self.force = list(np.loadtxt(filename, delimiter=delimiter, usecols=(forcecol,), skiprows=skiprows, dtype=float))
        self.true_cycleindexlist = [0, ]
        self.true_backbone = []
        self.true_paresult = []

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
            s = 0.5 * h * (l1 + l2)
            energy += s
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
        if slope > 0:
            for i in range(begin, end):
                if searchlist[i - 1] < searchpoint <= searchlist[i]:
                    pointindex = i
                    break
        elif slope < 0:
            for i in range(begin, end):
                if searchlist[i - 1] > searchpoint >= searchlist[i]:
                    pointindex = i
                    break
        else:
            pointindex = 'NA'
        return pointindex

    @staticmethod
    def interpolation(point1, list1, list2):
        """
        :param point1:
        :param list1:
        :param list2:
        :return: point2
        """
        point2 = 'NA'
        for i in range(len(list1) - 1):
            if list1[i] < point1 <= list1[i+1]:
                k = (list2[i+1] - list2[i]) / (list1[i+1] - list1[i])
                point2 = list2[i] + k * (point1 - list1[i])
                break
        return point2

    @property
    def cycleindexlist(self):
        """
        :return: index list for the first point of each cycle
        """
        for i in range(len(self.disp)-1):
            if self.disp[i] <= 0 < self.disp[i + 1] and i - self.true_cycleindexlist[-1] > 3:
                self.true_cycleindexlist.append(i+1)
        flag = self.true_cycleindexlist[-1] - len(self.disp) + 1
        if flag in (-10, 10):
            self.true_cycleindexlist.append(len(self.disp)-1)
        return self.true_cycleindexlist

    @property
    def backbone(self):
        """
        :return: [disp,force] of backbone curve
        """
        # Get disordered backbone data
        backboneforce_list_disordered = [0, ]
        backbonedisp_list_disordered = [0, ]
        maxdisp_hist = 0
        mindisp_hist = 0
        for i in range(len(self.cycleindexlist)-1):
            begin = self.cycleindexlist[i]
            end = self.cycleindexlist[i + 1]
            cycleforce_list = self.force[begin:end]
            cycledisp_list = self.disp[begin:end]
            maxdisp = max(cycledisp_list)
            mindisp = min(cycledisp_list)
            # add point corresponding to max force in this cycle
            if maxdisp_hist < maxdisp:
                maxdisp_hist = maxdisp
                maxforce = max(cycleforce_list)
                maxforce_index = cycleforce_list.index(maxforce)
                maxforce_disp = cycledisp_list[maxforce_index]
                backboneforce_list_disordered.append(maxforce)
                backbonedisp_list_disordered.append(maxforce_disp)
            # add point corresponding to min force in this cycle
            if mindisp_hist > mindisp:
                mindisp_hist = mindisp
                minforce = min(cycleforce_list)
                minforce_index = cycleforce_list.index(minforce)
                minforce_disp = cycledisp_list[minforce_index]
                backboneforce_list_disordered.append(minforce)
                backbonedisp_list_disordered.append(minforce_disp)
            if i == len(self.cycleindexlist) - 1:
                break
        # Reorder backbone data
        backboneforce_list = []
        backbonedisp_list = []
        for i in range(len(backbonedisp_list_disordered)):
            disp_selected = min(backbonedisp_list_disordered)
            index_selected = backbonedisp_list_disordered.index(disp_selected)
            force_selected = backboneforce_list_disordered[index_selected]
            backbonedisp_list.append(disp_selected)
            backboneforce_list.append(force_selected)
            del backbonedisp_list_disordered[index_selected]
            del backboneforce_list_disordered[index_selected]
        self.true_backbone = [backbonedisp_list, backboneforce_list]
        return self.true_backbone

    @property
    def paresult(self):
        """
        :return:result for the parametric analysis in 2020
        """
        envelop_disp = [-36, -25.0, -18.0, -15.8, -12.0, -8.0, -4.0, -2.0, 0, 2.0, 4.0, 8.0, 12.0, 16.0, 18.0, 25.0, 36]
        envelop_force = [-1.171, -1.673, -2.105, -2.155, -2.061, -1.822, -1.465, -1.097, 0, 1.097, 1.462, 1.82, 2.06, 2.156, 2.115, 1.636, 1.186]
        fmaxhist_list = ["fmaxhist",]
        fun_p_list = ["fun_p",]
        fev_p_list = ["fev_p",]
        dun_p_list = ["dun_p",]
        dmaxhist_list = ["dmaxhist",]
        fi_p_list = ["fi_p",]
        fminhist_list = ["fminhist",]
        fun_n_list = ["fun_n",]
        fev_n_list = ["fev_n",]
        dun_n_list = ["dun_n",]
        dminhist_list = ["dminhist",]
        fi_n_list = ["fi_n",]
        fmaxhist = 0
        fminhist = 0
        dmaxhist = 0
        dminhist = 0
        fi_p = 0
        fi_n = 0
        for i in range(len(self.cycleindexlist)-1):
            begin = self.cycleindexlist[i]
            end = self.cycleindexlist[i + 1]
            cycleforce_list = self.force[begin:end]
            cycledisp_list = self.disp[begin:end]
            fmax = max(cycleforce_list)
            fmin = min(cycleforce_list)
            dun_p = max(cycledisp_list)
            dun_n = min(cycledisp_list)
            fun_p = cycleforce_list[(cycledisp_list.index(dun_p))]
            fun_n = cycleforce_list[(cycledisp_list.index(dun_n))]
            fev_p = self.interpolation(dun_p, envelop_disp, envelop_force)
            fev_n = self.interpolation(dun_n, envelop_disp, envelop_force)
            fmaxhist = max(fmaxhist, fmax)
            fminhist = min(fminhist, fmin)
            dmaxhist = max(dmaxhist, dun_p)
            dminhist = min(dminhist, dun_n)
            for k in range(len(cycledisp_list)-1):
                if cycledisp_list[k] > 0 >= cycledisp_list[k+1]:
                    fi_p = cycleforce_list[k+1]
                if cycledisp_list[k] < 0 <= cycledisp_list[k+1]:
                    fi_n = cycleforce_list[k+1]
            fmaxhist_list.append(fmaxhist)
            fun_p_list.append(fun_p)
            fev_p_list.append(fev_p)
            dun_p_list.append(dun_p)
            dmaxhist_list.append(dmaxhist)
            fi_p_list.append(fi_p)
            fminhist_list.append(fminhist)
            fun_n_list.append(fun_n)
            fev_n_list.append(fev_n)
            dun_n_list.append(dun_n)
            dminhist_list.append(dminhist)
            fi_n_list.append(fi_n)
        self.true_paresult = [fmaxhist_list, fun_p_list, fev_p_list, dun_p_list, dmaxhist_list, fi_p_list, fminhist_list, fun_n_list, fev_n_list, dun_n_list, dminhist_list, fi_n_list]
        return self.true_paresult

if __name__ == '__main__' :
    data1 = HYSTdata('data/HYSTresult-4a.txt', 0, 1, ',', 1)
    # print(data1.backbone)

    for i in range(len(data1.paresult[0])):
        for j in range(len(data1.paresult)):
            print(data1.paresult[j][i],end = ' ')
        print('')

