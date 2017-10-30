import pyrosetta
import sys
import os


pyrosetta.init()

names = sys.argv[1:]

total_pose = 0
pose_names = []

for name in names:
    pose = pyrosetta.pose_from_pdb(name)
    out = os.path.splitext(os.path.basename(name))[0] + '.tra1'
    pose_names.append(out)
    with open(out, 'wt') as f:
        f.write("%d 0.0 1 1\n" % pose.total_residue())
        for i in range(pose.total_residue()):
            f.write("%10.5f %10.5f %10.5f\n" % (pose.phi(i + 1), pose.psi(i + 1), pose.omega(i + 1)))

    total_pose += 1

with open('tra.in', 'wt') as f:
    f.write("%d\n" % total_pose)
    for name in pose_names:
        f.write("%s\n" % name)
