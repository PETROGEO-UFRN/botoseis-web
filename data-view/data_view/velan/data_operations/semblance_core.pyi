import numpy as np
import numpy.typing as np_types


class semblance_core:
    """
    Represents the compiled Fortran module `semblance_core`.

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

        Core function implemented in Fortran at `semblance_core.f90`

        ### Parameters:
            - coherence_matrix: Output. 
        """
        ...
