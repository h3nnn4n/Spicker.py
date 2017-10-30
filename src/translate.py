import pyrosetta
import sys


pyrosetta.init()

basename = sys.argv[1]
names = sys.argv[2:]

total_pose = 0
pose_names = []

plen = 0

out = basename + '.tra1'

with open(out, 'wt') as f:
    for name in names:
        pose = pyrosetta.pose_from_pdb(name)
        plen = pose.total_residue()
        pose_names.append(out)
        f.write("%d 0.0 %6d %6d\n" % (pose.total_residue(), total_pose + 1, total_pose + 1))
        for i in range(pose.total_residue()):
            for j in range(pose.residue(i + 1).natoms()):
                if pose.residue(i + 1).atom(j + 1).type() == 24:
                    coords = pose.residue(i + 1).atom(j + 1).xyz()
                    f.write("%10.3f %10.3f %10.3f\n" % (coords[1], coords[2], coords[3]))
                    break

    total_pose += 1

with open('tra.in', 'wt') as f:
    f.write("%d %d %d\n" % (total_pose, -1, 1))
    f.write("%s\n" % out)
    # for name in pose_names:
    #     f.write("%s\n" % name)

with open('rmsinp', 'wt') as f:
    f.write("%d %d\n" % (1, plen))
    f.write("%d\n" % (plen))

pose = pyrosetta.pose_from_pdb(names[0])
with open('seq.dat', 'wt') as f:
    for n in range(pose.total_residue()):
        f.write("%4d %3s\n" % (n + 1, pose.residue(n + 1).name3()))
