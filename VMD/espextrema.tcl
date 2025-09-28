# Set atom selections for Carbon and Oxygen atoms
set selCarbon [atomselect top "name C"]
set selOxygen [atomselect top "name O"]

# Get the coordinates and energy values (beta) for Carbon and Oxygen atoms
set carbonCoords [$selCarbon get {x y z}]
set carbonEnergies [$selCarbon get beta]
set oxygenCoords [$selOxygen get {x y z}]
set oxygenEnergies [$selOxygen get beta]

# Create annotations for Carbon (surface maxima) with their ESP values in kJ/mol
foreach coord $carbonCoords energy $carbonEnergies {
    set x [lindex $coord 0]
    set y [lindex $coord 1]
    set z [lindex $coord 2]
    # Convert energy from kcal/mol to kJ/mol
    set energy_kj [expr {$energy * 4.184}]
    # Draw text label without "kcal/mol"
    graphics top text [list $x $y $z] [format "%.2f" $energy_kj] size 1 thickness 2
    # Change color of the last drawn graphics to color index 1 (e.g., red)
    graphics top color 1
}

# Create annotations for Oxygen (surface minima) with their ESP values in kJ/mol
foreach coord $oxygenCoords energy $oxygenEnergies {
    set x [lindex $coord 0]
    set y [lindex $coord 1]
    set z [lindex $coord 2]
    # Convert energy from kcal/mol to kJ/mol
    set energy_kj [expr {$energy * 4.184}]
    # Draw text label without "kcal/mol"
    graphics top text [list $x $y $z] [format "%.2f" $energy_kj] size 1 thickness 2
    # Change color of the last drawn graphics to color index 4 (e.g., blue)
    graphics top color 4
}

# Delete selections to free memory
$selCarbon delete
$selOxygen delete
