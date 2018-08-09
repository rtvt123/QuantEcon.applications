using Plots
pyplot()

A = [1.0 2.0
     2.0 1.0]

xmin, xmax = -3, 3
ymin, ymax = -3, 3

evals, evecs = eig(A)

# Extract x and y values of each eigenvector, arrange for plotting
x_vals = [zeros(1, size(A, 1)); evecs[1,:]]
y_vals = [zeros(1, size(A, 1)); evecs[2,:]]

# Image of each eigenvector
evecs =(evecs[:,1], evecs[:,2])
images = [[] []]'
for v in evecs
  v = A * v
  images = hcat(images, v)
end

# Extract x and y values of each image, arrange for plotting
x_ims = [zeros(1, size(A, 1)); images[1, :]]
y_ims = [zeros(1, size(A, 1)); images[2, :]]

x = linspace(xmin, xmax, 3)
as = []
for v in evecs
    a = v[2] / v[1]
    push!(as, a .* x)
end

# Plot each vector and its image
plot(x_ims, y_ims, arrow=true, color=:red,
     legend=:none, linewidth=1.8)
plot!(x_vals, y_vals, arrow=:true, color=:blue,
      xlims=(xmin, xmax), ylims=(ymin, ymax),
      legend=:none, linewidth=1.8)
plot!(x, as, color=:black, linewidth=0.3)
vline!([0], color=:black)
hline!([0], color=:black)
plot!(foreground_color_axis=:white, foreground_color_text=:white,
      foreground_color_border=:white)
