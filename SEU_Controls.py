from time import sleep
from PowerSupplyControls import getPowerSupply


if __name__=='__main__':

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('--logging', default=False, action='store_true', help='Start power monitoring')
    parser.add_argument('--logName', default='logFile.log', help='log name')
    parser.add_argument('--time', default=15, type=float,help='Frequency (in seconds) of how often to read the power')
    parser.add_argument('--ip', default='192.168.1.50', help='IP Address of the gpib controller')
    parser.add_argument('--addr', default=8, type=int, nargs='+', choices=[3,4,6,8],help='GPIB address(es) of the power supply')
    parser.add_argument('--run_number', type=int, help='Run number to include in log file name')

    args = parser.parse_args()

    powerSupplies={}
    for address in args.addr:
        print(f'Connecting to power supply at address {address}...')
        powerSupplies[address]=getPowerSupply(args.ip,address)
    if args.logging:
        import logging
        import time
            
        logging.basicConfig(filename=args.logName,
                            level=logging.INFO,
                            format='%(asctime)4s %(message)s',
                            )
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)4s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)

        if args.run_number is not None:
            logging.info(f'Starting run number {args.run_number}')

        try:
            while True:
                for address,ps in powerSupplies.items():
                    ps.reconnect()
                    p,v_ASIC,i_ASIC=ps.ReadPower()
                    logging.info(f'Address: {address}, Power: {"On" if int(p) else "Off"}, ASIC Voltage: {float(v_ASIC):.4f}, ASIC Current:{float(i_ASIC):.4f}')
                    ps.disconnect()
                sleep(args.time)
        except KeyboardInterrupt:
            logging.info(f'Closing')
            if args.run_number is not None:
                logging.info(f'Ending run number {args.run_number}')


