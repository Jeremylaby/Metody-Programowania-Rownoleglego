mkdir -p results/pp
mpicc -o ping_pong_c ping_pong.c
echo "Inside one node PP comuncation"
mpiexec -machinefile ./onenode -np 2 ./ping_pong_c > results/pp/ping_pong_result_1.csv
echo "Between two nodes PP comunication"
mpiexec -machinefile ./twonode -np ./ping_pong_c > results/pp/ping_pong_result_2.csv
echo "Done"