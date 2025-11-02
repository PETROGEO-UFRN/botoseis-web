module semblance_core
   implicit none
   public

contains

   subroutine semblance(suCMPdata, offsets, velocities, t0_data, dt, nt, num_traces, velocities_length, coherence_matrix)
      integer, intent(in) :: nt, num_traces, velocities_length
      real, intent(in) :: suCMPdata(nt, num_traces)
      real, intent(in) :: offsets(num_traces), velocities(velocities_length)
      real, intent(in) :: t0_data, dt
      real, intent(out) :: coherence_matrix(nt, velocities_length)

      real, save :: timewincoer = 0.060
      integer :: i, j, k, iw, nw, iv, it
      real :: t0, v, hs, tshift, ftvt, frac
      real :: amplitude, sumamplitude, sumenergia, energiasomatracos, energiatracos
      real, allocatable :: t(:)

      allocate (t(num_traces))

      ! Calculando os indices para a janela temporal
      nw = nint((timewincoer/dt + 1)/2)  ! Numero de pontos para a metade da janela

      do iv = 1, velocities_length
         v = velocities(iv)
         do i = 2, nt - 1
            t0 = t0_data + (i - 1)*dt
            k = 0
            do j = 1, num_traces
               k = k + 1
               hs = offsets(j)/v
               t(k) = sqrt(t0*t0 + hs*hs)
            end do
            energiasomatracos = 0.0
            energiatracos = 0.0
            do iw = -nw, nw, 1
               tshift = dt*iw
               sumamplitude = 0.0
               sumenergia = 0.0
               k = 0
               do j = 1, num_traces
                  k = k + 1
                  ftvt = ((t(k) + tshift) - t0_data)/dt
                  it = 1 + int(ftvt)
                  frac = ftvt - int(ftvt)
                  if (it >= 1 .and. it <= (nt - 1)) then
                     amplitude = (1.-frac)*suCMPdata(it, j) + frac*suCMPdata(it + 1, j)
                     sumamplitude = sumamplitude + amplitude
                     sumenergia = sumenergia + amplitude*amplitude
                  end if
               end do
               energiasomatracos = energiasomatracos + sumamplitude*sumamplitude
               energiatracos = energiatracos + sumenergia
            end do
            coherence_matrix(i, iv) = energiasomatracos/(num_traces*energiatracos)
         end do
      end do
   end subroutine semblance

end module semblance_core
