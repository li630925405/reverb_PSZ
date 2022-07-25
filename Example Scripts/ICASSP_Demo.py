import sys 
sys.path.append("..") 
import pyzones as pz
import numpy as np
import os
import matplotlib.pyplot as plt


# Create a 4 x 4 m soundfield with origin at the center
size = 4
soundfield = pz.Soundfield([0, 0], size, size, coordinate_pos="centre")

# Create the zones, Zone(xy, radius)
# setting the colour of the zones is optional, this only affects the visualisation at the end.
bright_zone = pz.Zone([0, -0.5], 0.2, colour=(1, 1, 1))
# bright_zone = pz.Zone([0, -2], 0.2, colour=(1, 1, 1))
# dark2_zone = pz.Zone([0, 2], 0.11, colour=(0.5, 0.5, 0.5))
dark_zone = pz.Zone([0, 0.5], 0.2, colour=(0, 0, 0))
# dark_zone = pz.Zone([0, 2], 0.2, colour=(1, 1, 1))


# Add zones to soundfield
# soundfield.add_zones([bright_zone, dark2_zone, dark_zone])
soundfield.add_zones([bright_zone, dark_zone])

# Create an array of loudspeakers
# Demo: Circular Array automatically generated
#num_ls = 60
#ls_array = pz.LoudspeakerArray([pz.Loudspeaker() for _ in range(num_ls)])
#
## Define the shape of the loudspeaker array, Circle(xy, radius). Then position the loudspeakers around the shape.
#ls_array_shape = pz.Circle([0, 0], 1.680)
#ls_array.position_objects(ls_array_shape.get_perimeter(0, 0, num_ls))

# Demo: 10 element line array 10cm spacing
num_ls = 10
ls_array = pz.LoudspeakerArray([pz.Loudspeaker() for _ in range(num_ls)])
loudspeaker_positions = np.array([[1.68,-0.45],
                                  [1.68,-0.35],
                                  [1.68,-0.25],
                                  [1.68,-0.15],
                                  [1.68,-0.05],
                                  [1.68,0.05],
                                  [1.68,0.15],
                                  [1.68,0.25],
                                  [1.68,0.35],
                                  [1.68,0.45]])
ls_array.position_objects(loudspeaker_positions)

soundfield.add_sound_objects(ls_array)

# Create the microphone arrays
# 48 microphones evenly spaced around each zone perimeter for setup
# and 48 microphones, offset by 3.75 deg., around each zone perimeter for evaluation
num_mics_per_circle = 4

bright_setup = pz.MicrophoneArray([pz.Microphone("bright", "setup") for _ in range(num_mics_per_circle)])
bright_setup.position_objects(bright_zone.get_perimeter(0, 0, num_mics_per_circle))

bright_eval = pz.MicrophoneArray([pz.Microphone("bright", "evaluation") for _ in range(num_mics_per_circle)])
bright_eval.position_objects(bright_zone.get_perimeter(3.75, 3.75, num_mics_per_circle))

# dark2_setup = pz.MicrophoneArray([pz.Microphone("dark", "setup") for _ in range(num_mics_per_circle)])
# dark2_setup.position_objects(dark2_zone.get_perimeter(0, 0, num_mics_per_circle))

# dark2_eval = pz.MicrophoneArray([pz.Microphone("dark", "evaluation") for _ in range(num_mics_per_circle)])
# dark2_eval.position_objects(dark2_zone.get_perimeter(3.75, 3.75, num_mics_per_circle))


dark_setup = pz.MicrophoneArray([pz.Microphone("dark", "setup") for _ in range(num_mics_per_circle)])
dark_setup.position_objects(dark_zone.get_perimeter(0, 0, num_mics_per_circle))

dark_eval = pz.MicrophoneArray([pz.Microphone("dark", "evaluation") for _ in range(num_mics_per_circle)])
dark_eval.position_objects(dark_zone.get_perimeter(3.75, 3.75, num_mics_per_circle))

# Combine microphone arrays
mic_array = bright_setup + bright_eval + dark_setup + dark_eval
# mic_array = bright_setup + bright_eval + dark2_setup + dark2_eval + dark_setup + dark_eval

soundfield.add_sound_objects(mic_array)

# Frequencies to test
frequencies = np.arange(0, 22050, 5)
# frequencies = np.arange(0, 20480, 20)  # 1024

# Create your simulation, optional arguments are available to set constants
# simulation和soundfield是分开的吗？好奇怪

# Choose the method used - ACC, PM, etc.
methods = ['ACC']
# methods = ['BC', 'ACC', 'PM']
vis_tfs = None
grid = None

# savepath = "%s/Research/ICASSPTutorial2019/Demo" % os.environ['HOME']
# sim = pz.Simulation(frequencies, ls_array, mic_array, pm_angle=90, reverb_order=0)

effort = []
contrast = []
size_range = [4]

reverb_order = 3
for size in size_range:
    for method in methods:
        # sim.set_reverb_order(reverb_order=reverb_order)
        sim = pz.Simulation(frequencies, ls_array, mic_array, size=size, pm_angle=90, reverb_order=reverb_order)
        print("*********  begin initialization ********* ")
        # Run your simulation by calculating the filter weights and subsequently evaluate these by calculating metrics
        print("********* calculating weights ********* ")
        sim.calculate_filter_weights(method=method,beta=10e-3)
        metrics = sim.calculate_metrics(contrast=True, effort=True)

        # reverberation as x axis
        # print(metrics._metrics[:, 0])  # contrast
        # contrast.append(sum(metrics._metrics[:, 0])/len(frequencies))
        # effort.append(sum(metrics._metrics[:, 1])/len(frequencies))

        # print("*********  begin evaluation ********* ")
        #metrics.print(contrast=True, effort=True)
        # metrics.output_csv("0620/results_%s_reverb_%s.csv" % (method, reverb_order), overwrite=True, contrast=True, effort=True)
        
        # plot the results over frequency
        metrics.plot("%s Contrast" % method, "0725/%s_contrast_reverb_%s_no tf.png" % (method, reverb_order), "contrast")
        metrics.plot("%s Effort" % method, "0725/%s_effot_reverb_%s_no tf.png" % (method, reverb_order), "effort")

        # print("*********  beigin visualization ********* ")
        # Create the soundfield visualisation for the most recently calculated filter weights and choose the frequency at
        # which is it visualised
        vis_frequency = 1000
        vis_tfs, grid = soundfield.visualise(sim, "0725/%s-%dHz_reverb_%s_pressure_no tf.png" % (method, vis_frequency, reverb_order), frequency=vis_frequency, sf_spacing=0.1,transfer_functions=vis_tfs, grid=grid)
        
        # soundfield.auralize(sim)


# plt.figure(figsize=(10, 3))
# plt.subplot(1, 2, 1)
# plt.plot(contrast)
# plt.subplot(1, 2, 2)
# plt.plot(effort)
# plt.show()
