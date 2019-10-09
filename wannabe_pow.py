# How the real-life proof-of-work should go

CONFIG = {

}
    

DATA_DIR = "/home/pachacho/Documents/anafi_tools/data/pow"

OPTITRACK_FPATH = ""

if __name__ == "__main__":

    # engine = tensorflow.load_model("my_model.tf")

    for i in range(CONFIG["runs"]):
        print_start("Starting run no. {}".format(i))

        try:
            print("Launch Optitrack (external to this script!)")

            BackgroundTask(
                "roscore",
                log=True, log_file="", wait=5
            )
            
            BackgroundTask(
                "ros2 run ros1_bridge dynamic_bridge --bridge-all-1to2-topics",
                log=True, log_file="", wait=5
            )
            
            BackgroundTask(
                "roslaunch vrpn_client_ros sample.launch server:=192.168.101.93:3883",
                log=True, log_file="", wait=5
            )
            
            # drone = AnafiControl(AnafiControl.PHYSICAL_IP)
            # drone.set_vel([0,0,1,0,0,0])

            # This node reads from optitrack topics, computes distances-forces
            # then pass them to the used "engine" and finally sends it to
            # the drone through olympe (POW_IP for real drone, SIM_IP otherwise)
            runner = MasterNode(
                simulated=False,
                model=engine,
                ip = MasterNode.POW_IP,
                logfile=OPTITRACK_FPATH
            )

            # Wait until the drone lands i.e. the simulation ends
            opti.wait()

        except KeyboardInterrupt as e:
            print_error("CTRL+C has been pressed! Exiting")
            # If the run is interrumpted, do an emergency land
            opti.emergency_land()
