import argparse

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from .camera import Camera
from .log import logger

URL_PATH_MJPG = '/camera.mjpg'
URL_PATH_FAVICON = '/favicon.ico'
SLEEP_IN_SEC = 0.050


class CameraHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.document_root = server.get_document_root()
        self.camera = server.get_camera()
        super(CameraHandler, self).__init__(request, client_address, server)

    def do_GET(self):
        if self.path == URL_PATH_MJPG:
            self.send_response(200)
            self.send_header(
                'Content-type',
                'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while self.camera.is_opened():
                jpg = self.camera.read_in_jpeg(SLEEP_IN_SEC)
                if jpg is None:
                    continue
                self.wfile.write("--jpgboundary".encode())
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', str(jpg.nbytes))
                self.end_headers()
                self.wfile.write(jpg)
        elif self.path == URL_PATH_FAVICON:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('favicon is not found'.encode())
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(self.document_root + '/index.html', 'r') as f:
                self.wfile.write(f.read().encode())
        logger.info('thread is stopping ... [{path}]'.format(path=self.path))


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    def set_camera(self, camera):
        self.camera = camera

    def get_camera(self):
        return self.camera

    def set_document_root(self, document_root):
        self.document_root = document_root

    def get_document_root(self):
        return self.document_root


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8080)
    parser.add_argument('--width', type=int, default=320)
    parser.add_argument('--height', type=int, default=240)
    parser.add_argument('--directory', type=str, default='html')
    parser.add_argument('--device-index', type=int, default=0)
    args = parser.parse_args()

    camera = Camera(args.device_index, args.width, args.height)
    try:
        server = ThreadedHTTPServer((args.bind, args.port), CameraHandler)
        server.set_camera(camera)
        server.set_document_root(args.directory)
        logger.info("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("server is stopping ...")
        camera.release()
        server.shutdown()


if __name__ == '__main__':
    main()
