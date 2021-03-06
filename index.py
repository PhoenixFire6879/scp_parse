from utils.reader import Reader
import os



def _(string):
    print(f"[INFO] {string}")


class ScP():
    def __init__(self, filename):
        data = open(filename, 'rb').read()
        self.initial_file = filename
        self.r = Reader(data)


    def scp_parse(self):
        # scp header
        signature = self.r.read(4)

        if signature == b'SCP!':

            version = self.r.read_int32()

            _(f"SCP version is {version}\n")

            self.r.read_int32()

            self.files_count = self.r.read_int32() # files count
            info_offset      = self.r.read_int32() # files info offset

            self.r.read_int64()
            self.r.read_int64()

            for i in range(9):
                self.r.read_int32()

            self.r.read_hash(32) # maybe a kind of hash

            self.r.skip(1)

        # scp header ends here

            self.r.set_offset(info_offset)

            for i in range(self.files_count):

                self.r.read_int16()
                self.r.read_int16() # file name length

                self.file_size   = self.r.read_int64()
                self.file_offset = self.r.read_int64()
                self.file_size   = self.r.read_int64()

                self.file_hash   = self.r.read_hash(32)
                self.file_name   = self.r.read_string_little()

                offset           = self.r.stream.tell()
                self.r.set_offset(self.file_offset)

                self.file_data   = self.r.read(self.file_size)

                _(f"Parsed file! Name: {self.file_name}, hash: {self.file_hash}, size: {self.file_size}, offset: {self.file_offset}")
                self.r.set_offset(offset)

                self.save(self.file_name, self.initial_file, self.file_data)

            return self.files_count, self.file_name, self.initial_file, self.file_data
        else:
            _(f"Wrong file signature: {str(signature)}. Returning!")



    def save(self, filename, initial, file_data):
        a = filename.split('\\')[-1].split('.')[0]
        b = initial.split('\\')[-1].split('.')[0]

        try:
            if not os.path.isdir(f'{b}/{a}'):
                os.makedirs(f'{b}/{a}')

            file = open(f'{b}/{a}/{filename}', 'wb')
            file.write(file_data)
            file.close()
            _(f"File saved to {b}/{a}/{filename}")

        except Exception as e:
            _(f"Unexpected error: {e}")



input_file = input("Enter the name of the scp (eg. tutorial.scp)\n")

parser = ScP(input_file)
parser.scp_parse()
