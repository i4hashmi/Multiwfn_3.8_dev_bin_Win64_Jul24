set all [atomselect top all]
set num_atoms [$all num]

for {set i 0} {$i < $num_atoms} {incr i} {
    set sel [atomselect top "index $i"]
    set esp [$sel get beta]
    set coords [$sel get {x y z}]
    
    # Convert energy from kcal/mol to kJ/mol
    set esp_kj [expr {$esp * 4.184}]
	
	# Format ESP to 2 decimal places
    set esp_formatted [format "%.1f" $esp_kj]
	    
    # Shift x coordinate by 0.25
    set x [expr {[lindex $coords 0 0] + 0.25}]
    set y [lindex $coords 0 1]
    set z [lindex $coords 0 2]
    
    # Create label with shifted position and black color
    draw color black
    draw text "$x $y $z" "$esp_formatted" size 1.0 thickness 2
    
    $sel delete
}