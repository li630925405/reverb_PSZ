class Reverb:
    def calculate_ir(self, size=20, sources, mics, order=1, sr=22050, f=500):
        c = 340
        # sources = np.array([[18, 15]])
        # mic = [15, 15]
        dist = []
        # 共采样sr个点，这样fft后每个频点的n就是相应的频率
        IR = np.zeros(sr)
        tf = np.zeros(mics.shape)

        for i in range(order):
            for source in sources:
                img = []
                img.append([-source[0], source[1]])
                img.append([size - source[0] + size, source[1]])
                img.append([source[0], -source[1]])
                img.append([source[0], size - source[1] + size])
                img = np.array(img)
                # print("img: ", img)
                sources = np.append(sources, img, axis=0)
                sources = np.unique(sources, axis=0)
                # print(sources)
                i += 1
                if i > order:
                break

        for i, mic in enumerate(mics):
            for source in sources:
                dist.append(math.sqrt((source[0] - mic[0])**2 + (source[1] - mic[1])**2))

            for d in dist:
                # print(d / c)
                IR[int(d * sr // c)] = min(1 / d * 10 + IR[int(d * sr // c)], 1)
                tf[i] = np.fft.fft(IR)[f]

        return tf