import cv2
# from pyspin import PySpin
from simple_pyspin import Camera


logger = logging.getLogger(__name__)


class Camera(object):
    def __init__(self, cam):
        self.cam = cam
        self.cam.Init()

    def stop(self):
        logger.debug('Cleaning up')
        self.cam.DeInit()
        del self.cam
        self.cam = None

    def configure(self):
        self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
        self.cam.PixelFormat.SetValue(PySpin.PixelFormat_BayerRG8)
        self.cam.BinningHorizontal.SetValue(2)
        self.cam.BinningVertical.SetValue(2)
        self.cam.Width.SetValue(1920)
        self.cam.Height.SetValue(1080)
        self.cam.AcquisitionFrameRateEnable.SetValue(True)
        self.cam.AcquisitionFrameRate.SetValue(30)
        self.cam.TLStream.StreamBufferCountMode.SetValue(
            PySpin.StreamBufferCountMode_Manual)
        self.cam.TLStream.StreamBufferCountManual.SetValue(1)
        self.cam.TLStream.StreamBufferHandlingMode.SetValue(
            PySpin.StreamBufferHandlingMode_NewestOnly)

    def show_image(self, data):
        cv2.imshow('image', data)
        cv2.waitKey(1)

    def run(self):
        logger.debug('Starting')
        self.configure()
        self.cam.BeginAcquisition()
        try:
            logger.debug('Streaming')
            while True:
                img = self.cam.GetNextImage()
                if img.IsIncomplete():
                    logger.warning('Image incomplete (%d)',
                                   img.GetImageStatus())
                    continue

                img_conv = img.Convert(PySpin.PixelFormat_BGR8,
                                       PySpin.HQ_LINEAR)
                # or img.GetData().tobytes() for pushing into gstreamer buffers
                self.show_image(img_conv.GetNDArray())
                img.Release()

        except PySpin.SpinnakerException as e:
            logger.exception(e)
        finally:
            logger.debug('Ending')
            self.cam.EndAcquisition()


def main():
    logging.basicConfig(level=logging.DEBUG)
    system = PySpin.System.GetInstance()
    version = system.GetLibraryVersion()
    logger.debug('Library version: %d.%d.%d.%d',
                 version.major, version.minor, version.type, version.build)
    cam_list = system.GetCameras()
    if not cam_list.GetSize():
        logger.error('No cameras found')
        return
    cam = cam_list[0]
    del cam_list
    camera = Camera(cam)
    try:
        camera.run()
    except KeyboardInterrupt:
        pass
    finally:
        camera.stop()
        system.ReleaseInstance()


if __name__ == '__main__':
    main()