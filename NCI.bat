@echo off
(
echo 20
echo 1
echo 2
echo 2
echo 3
) | Multiwfn CF3_opt_g16.fch

move /Y func1.cub "D:\Multiwfn_3.8_dev_bin_Win64_Jul24\VMD"
move /Y func2.cub "D:\Multiwfn_3.8_dev_bin_Win64_Jul24\VMD"
move /Y output.txt "D:\Multiwfn_3.8_dev_bin_Win64_Jul24\gnuplot\bin"

echo.
echo Analysis complete. Press any key to close.
::pause
