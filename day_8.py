if __name__ == "__main__":
    n = 6
    m = 25
    file = open("input.txt","r")
    file_str = file.read()
    layers = [file_str[i*n*m:(i+1)*n*m] for i in range(len(file_str) // (n*m))]
    special_layer = layers[0]
    for layer in layers:
        if special_layer.count("0") > layer.count("0"):
            special_layer = layer
    print("#(1 digits) * #(2 digits) in described layer is", special_layer.count("1")*special_layer.count("2"))

    color = [[2]*m for i in range(n)]

    for layer in layers:
        for i in range(n):
            for j in range(m):
                pixel = int(layer[i*m + j])
                if pixel != 2 and color[i][j] == 2:
                    color[i][j] = pixel

    for i in range(n):
        for j in range(m):
            if color[i][j] == 0:
                print(" ", end="")
            else:
                print("*", end="")
        print("")
