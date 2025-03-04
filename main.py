import tkinter as tk
from tkinter import ttk, messagebox
from Graph import Graph, DijkstrasSP, DijkstrasST, DijkstrasCP, PrintPath

# Load Graph Data
graph = Graph()
graph.nv = 0  # Initialize vertex count

# Load Edge Weights (Distances)
try:
    with open("Edgeweight.txt", "r") as file:
        for line in file:
            l = line.strip().split()
            if l:
                graph.AddEdge(l[0], l[1], float(l[2]))
except FileNotFoundError:
    messagebox.showerror("Error", "Edgeweight.txt file not found!")

# Load Bus Route Information
try:
    with open("BUS.TXT", "r") as file:
        first_line = file.readline().strip().split()
        bus_type = first_line.pop(0)
        graph.UpdateBusInfo(bus_type, first_line)

        for line in file:
            l = line.strip().split()
            bus_type = l.pop(0)
            graph.UpdateBusInfo(bus_type, l)
except FileNotFoundError:
    messagebox.showerror("Error", "BUS.TXT file not found!")

# Get list of available locations
locations = list(graph.GetVertices())

# Create Tkinter GUI
root = tk.Tk()
root.title("Bus Route Planner")
root.geometry("500x400")

# Title
tk.Label(root, text="Bus Route Planner", font=("Arial", 16, "bold")).pack(pady=10)

# Frame for Input Fields
frame = tk.Frame(root)
frame.pack(pady=10)

# Source Dropdown
tk.Label(frame, text="Source:").grid(row=0, column=0, padx=5)
source_var = tk.StringVar()
source_dropdown = ttk.Combobox(frame, textvariable=source_var, values=locations)
source_dropdown.grid(row=0, column=1)

# Destination Dropdown
tk.Label(frame, text="Destination:").grid(row=1, column=0, padx=5)
destination_var = tk.StringVar()
destination_dropdown = ttk.Combobox(frame, textvariable=destination_var, values=locations)
destination_dropdown.grid(row=1, column=1)

# Travel Mode Selection
tk.Label(root, text="Travel Mode:", font=("Arial", 12)).pack(pady=5)
mode_var = tk.IntVar(value=2)
tk.Radiobutton(root, text="Own Transport (Car, Motorcycle)", variable=mode_var, value=1).pack()
tk.Radiobutton(root, text="Public Transport (Bus)", variable=mode_var, value=2).pack()

# Priority Selection for Public Transport
priority_frame = tk.Frame(root)
priority_frame.pack(pady=5)
priority_var = tk.IntVar(value=1)

tk.Label(priority_frame, text="Choose Priority:", font=("Arial", 12)).pack(anchor="w")
tk.Radiobutton(priority_frame, text="Shortest Time", variable=priority_var, value=1).pack(anchor="w")
tk.Radiobutton(priority_frame, text="Cheapest Price", variable=priority_var, value=2).pack(anchor="w")

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12), wraplength=450, justify="left")
result_label.pack(pady=10)

# Find Route Function
def find_route():
    source = source_var.get()
    destination = destination_var.get()
    mode = mode_var.get()
    priority = priority_var.get()

    if not source or not destination:
        messagebox.showwarning("Input Error", "Please select both source and destination.")
        return
    if source == destination:
        messagebox.showwarning("Input Error", "Source and destination cannot be the same.")
        return

    # Reset graph values
    for vertex in graph.Vertices.values():
        vertex.ds = float("inf")
        vertex.ts = float("inf")
        vertex.cs = float("inf")
        vertex.parent = None
        vertex.busFrom = None

    # Calculate the shortest path based on mode and priority
    if mode == 1:  # Own Transport
        DijkstrasSP(graph, graph.GetVertex(source), graph.GetVertex(destination))
        result = f"Route: {source}"
        PrintPath(graph, source, destination)
        result += f"\nDistance: {graph.GetVertex(destination).ds} km"

    elif mode == 2:  # Public Transport
        if priority == 1:
            DijkstrasST(graph, graph.GetVertex(source), graph.GetVertex(destination))
            result = f"Route: {source}"
            PrintPath(graph, source, destination)
            result += f"\nTime Taken: {round(graph.GetVertex(destination).ts * 60, 2)} minutes"
        elif priority == 2:
            DijkstrasCP(graph, graph.GetVertex(source), graph.GetVertex(destination))
            result = f"Route: {source}"
            PrintPath(graph, source, destination)
            result += f"\nCost: Rs. {round(graph.GetVertex(destination).cs, 2)}"

    else:
        result = "Invalid selection"

    result_label.config(text=result)

# Find Route Button
find_button = tk.Button(root, text="Find Route", command=find_route, font=("Arial", 12))
find_button.pack(pady=10)

# Run Tkinter
root.mainloop()
