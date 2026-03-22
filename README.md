# Metody Programowania Równoległego

Repozytorium zawiera materiały i sprawozdania z laboratorium **Metody Programowania Równoległego** prowadzonego na kierunku Informatyka, Wydział Informatyki, AGH.

Przedmiot wprowadza w tematykę dużych systemów obliczeniowych, programowania równoległego i jego efektywności. W trakcie laboratoriów studenci tworzą programy wykorzystujące komunikację między procesami (MPI), współdzieloną pamięć (OpenMP) oraz obliczenia na kartach graficznych (CUDA), a następnie badają skalowalność i wydajność takich rozwiązań.

## Środowisko obliczeniowe

Eksperymenty prowadzone są w ramach grantu obliczeniowego **PLG/2025/017214** w infrastrukturze [PLGrid](https://www.plgrid.pl):

- **vCluster** — środowisko testowe, używane do weryfikacji poprawności programów przed właściwymi pomiarami
- **Ares** (ACK Cyfronet AGH) — superkomputer używany do właściwych pomiarów wydajnościowych; eksperymenty ograniczone do jednego węzła obliczeniowego (1–12 rdzeni), realizowane przez system kolejkowy SLURM

## Sprawozdania

### Sprawozdanie 1 — Komunikacja P2P i przybliżanie π metodą Monte Carlo

Sprawozdanie składa się z dwóch części:

- **Część 1** — pomiary przepustowości i opóźnienia komunikacji punkt-punkt (MPI\_Send/MPI\_Recv) na vClusterze w dwóch konfiguracjach: komunikacja wewnątrz jednego węzła oraz między dwoma węzłami
- **Część 2** — analiza skalowalności programu przybliżającego liczbę π metodą Monte Carlo na superkomputerze Ares; skalowanie silne i słabe dla trzech rozmiarów problemu

📄 [Sprawozdanie MPI (PDF)](lab-03-mpi/MPI_Sprawozdanie.pdf)