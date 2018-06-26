
subroutine gen_gauss(world, gauss)

  implicit none

! compile with f2py3 -c -m gen_gauss g_gauss_f.f90
  real*8, dimension(10,10,10) :: world
  real*8, dimension(10,10) :: gauss
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) gauss

  do x=1, 10
    do y=1, 10
      do z=1, 10
        !write(*,*) gauss(y,z), exp(-gauss(y,z))
        world(x,y,z) = exp(-abs((float(x)-gauss(y,z)))*5)
        !write(*,*) gauss(y,z), exp(-gauss(y,z)), exp(-gauss(y,z)), world(x,y,z)
        !write(*,*) gauss(y,z), -gauss(y,z), exp(float(0)), exp(-gauss(y,z))
      end do
    end do
  end do

end subroutine gen_gauss
