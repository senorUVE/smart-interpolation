import os   #скрипт пройдётся по папке, которую укажем, и разобьёт все .wav-файлы, которые он там встретит, на блоки длиной 1024 сэмпла и сохранит в другую указанную папку
import soundfile as sf
import numpy as np

snd_dir = "D:\\hl2_sound\\"
blocks_dir = "D:\\hl2_blocks\\"
block_len = 1024

for root, subdirs, files in os.walk(snd_dir):
    for file in files:
        if file.endswith(".wav"):
            print(os.path.join(root, file))
            file_stripped = file.replace(" ", "")
            i = 0
            file_blocksdir = os.path.splitext(os.path.join(blocks_dir, file_stripped))[0]
            if not os.path.isdir(file_blocksdir):
                os.mkdir(file_blocksdir)
            else:
                j = 0
                while os.path.isdir(os.path.splitext(os.path.join(blocks_dir, file_stripped))[0] + '{0:05d}'.format(j)):
                    j += 1
                os.mkdir(os.path.splitext(os.path.join(blocks_dir, file_stripped))[0] + '{0:05d}'.format(j))
            _, fsample_rate = sf.read(os.path.join(root, file))
            for block in sf.blocks(os.path.join(root, file),
                                   blocksize=block_len,
                                   overlap=0,
                                   fill_value=0):
                if np.sqrt(np.mean(block**2)) > 0.0:
                    if block.shape == (block_len,):
                        block_k = [x for x in block]
                        sf.write(os.path.splitext(os.path.join(file_blocksdir, file_stripped))[0] + "_block" + '_{0:05d}'.format(i) + ".wav",
                                 block_k,
                                 fsample_rate)
                    else:
                        blocks = []
                        for k in range(block.shape[1]):
                            block_k = [x[k] for x in block]
                            sf.write(os.path.splitext(os.path.join(file_blocksdir, file_stripped))[0] + "_block" + '_{0:1d}'.format(k) + '_{0:05d}'.format(i) + ".wav",
                                     block_k,
                                     fsample_rate)
                    i += 1
