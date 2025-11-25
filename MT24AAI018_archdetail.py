# nlp assignment 01 - Cohort 2 i. Type of layer
# ii. For a convolution layer, height of filter kernel, width of filter kernel,
# stride, padding, number of filter kernels. For a dense layer, number of
# nodes.
# iii. Dimension of the input.

print("\n Tuhin Roychowdhury - MT24AAI018")



import matplotlib.pyplot as plt

def layer_calc(layer_type, inp_dim, **args):
    if layer_type == "conv":
        h_in, w_in, ch_in = inp_dim
        kh = args.get("kh")
        kw = args.get("kw")
        s = args.get("stride", 1)
        p = args.get("pad", 0)
        f = args.get("filters")

        h_out = ((h_in - kh + 2*p)//s) + 1
        w_out = ((w_in - kw + 2*p)//s) + 1
        out_dim = (h_out, w_out, f)

        params = (kh * kw * ch_in + 1) * f
        dots = h_out * w_out * f
        per_dot = kh * kw * ch_in
        total = dots * (per_dot + (per_dot - 1))

        return out_dim, params, dots, total

    elif layer_type == "dense":
        (nin,) = inp_dim
        nout = args.get("nodes")

        out_dim = (nout,)
        params = (nin + 1) * nout
        dots = nout
        total = dots * (nin + (nin - 1))

        return out_dim, params, dots, total

    else:
        return None


if __name__ == "__main__":
    print("\nQ1: Example Runs ")
    conv_ex = layer_calc("conv", (32,32,3), kh=3, kw=3, stride=1, pad=1, filters=16)
    print("Conv Example (32x32x3, 3x3, 16 filters):", conv_ex)

    dense_ex = layer_calc("dense", (128,), nodes=64)
    print("Dense Example (128 -> 64):", dense_ex)

    # Plots for lab report
    plt.figure()
    plt.bar(["Params","Dot Products","Total Ops"], conv_ex[1:])
    plt.title("Conv Example Load")
    plt.savefig("conv_example_plot.png", dpi=300)

    plt.figure()
    plt.bar(["Params","Dot Products","Total Ops"], dense_ex[1:])
    plt.title("Dense Example Load")
    plt.savefig("dense_example_plot.png", dpi=300)

    print("\nQ2: GoogleNet Layers")
    conv1 = layer_calc("conv", (224,224,3), kh=7, kw=7, stride=2, pad=3, filters=64)
    print("Conv1 (7x7, stride 2, 64 filters):", conv1)

    conv2 = layer_calc("conv", (56,56,64), kh=3, kw=3, stride=1, pad=1, filters=192)
    print("Conv2 (3x3, stride 1, 192 filters):", conv2)

    fc = layer_calc("dense", (1024,), nodes=1000)
    print("Final Dense (1024 -> 1000):", fc)

    # Plot GoogleNet results
    plt.figure()
    labels = ["Conv1","Conv2","FC"]
    params = [conv1[1], conv2[1], fc[1]]
    plt.bar(labels, params)
    plt.title("GoogleNet Layers - Trainable Params")
    plt.savefig("googlenet_params.png", dpi=300)

    plt.figure()
    ops = [conv1[3], conv2[3], fc[3]]
    plt.bar(labels, ops)
    plt.title("GoogleNet Layers - Total Ops")
    plt.savefig("googlenet_ops.png", dpi=300)

    print("\nPlots saved: conv_example_plot.png, dense_example_plot.png, googlenet_params.png, googlenet_ops.png")
