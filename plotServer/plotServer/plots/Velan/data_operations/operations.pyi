import numpy.typing as np_types


class operations:
    """
    Represents the compiled Fortran module `operations`.

    Acts as a container for the functions/routines
    """

    def semblance(
        # *** Arguments must exactly match the f2py-generated signature
        sucmpdata: np_types.NDArray,
        offsets: np_types.NDArray,
        velocities: np_types.NDArray,
        t0_data: float,
        dt: float,
        nt: int,
        num_traces: int,
        velocities_length: int,
        # *** coherence_matrix is the output
        coherence_matrix: np_types.NDArray,
    ) -> np_types.NDArray:
        """
        Wrapping function for semblance coherency calculation.

        Core function implemented in Fortran at `operations.f90`

        ### Parameters:
            - coherence_matrix: Output. 
        """
        ...

    def velocity_picks_to_trace(
        npicks: int,
        tnmo: any,  # =picks_times,
        vnmo: any,  # =picks_velocities,
        t0_data: float,
        dt: float,
        nt: int,
    ) -> np_types.NDArray:
        """
        Core function implemented in Fortran at `operations.f90`

        ### Parameters:
            - vnmo_trace: Output. 
        """
        ...

    def apply_nmo(
        ntracescmp: int,
        nt: int,
        t0_data: float,
        dt: float,
        cmpdata: np_types.NDArray,
        offsets: np_types.NDArray,
        vnmo_trace: np_types.NDArray,
        smute: float,
    ) -> np_types.NDArray:
        """
        Wrapping function for nmo calculation.

        Core function implemented in Fortran at `operations.f90`

        ### Parameters:
            - CMPdata_nmo: Output. 
        """
        ...
