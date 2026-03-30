import mpi.*;

public class PingPong {

    static final int REPEATS = 1000;

    public static void main(String[] args) throws Exception {
        MPI.Init(args);

        int rank = MPI.COMM_WORLD.Rank();
        int size = MPI.COMM_WORLD.Size();

        if (size != 2) {
            if (rank == 0)
                System.err.println("Uruchom z dokladnie 2 procesami: mpirun -np 2");
            MPI.Finalize();
            return;
        }

        /* rozmiary komunikatow w bajtach */
        int[] sizes = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512,
                       1024, 4096, 16384, 65536, 262144, 1048576,
                       4194304, 16777216};

        if (rank == 0)
            System.out.println("size_bytes,bandwidth_mbit_s,latency_ms");

        for (int i = 0; i < sizes.length; i++) {
            int msgSize = sizes[i];
            byte[] buf = new byte[msgSize];

            MPI.COMM_WORLD.Barrier();
            double tStart = MPI.Wtime();

            for (int r = 0; r < REPEATS; r++) {
                if (rank == 0) {
                    MPI.COMM_WORLD.Send(buf, 0, msgSize, MPI.BYTE, 1, 0);
                    MPI.COMM_WORLD.Recv(buf, 0, msgSize, MPI.BYTE, 1, 0);
                } else {
                    MPI.COMM_WORLD.Recv(buf, 0, msgSize, MPI.BYTE, 0, 0);
                    MPI.COMM_WORLD.Send(buf, 0, msgSize, MPI.BYTE, 0, 0);
                }
            }

            double tEnd = MPI.Wtime();

            if (rank == 0) {
                /* czas jednego pelnego round-trip */
                double tRoundtrip = (tEnd - tStart) / REPEATS;
                /* opoznienie = polowa round-trip */
                double latencyMs = tRoundtrip / 2.0 * 1000.0;
                /* przepustowosc: 2 * msgSize bo tam i z powrotem */
                double bandwidth = (2.0 * msgSize * 8.0) /
                                   (tRoundtrip * 1e6);
                System.out.printf("%d,%.4f,%.6f%n", msgSize, bandwidth, latencyMs);
            }
        }

        MPI.Finalize();
    }
}