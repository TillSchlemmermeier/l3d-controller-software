
subroutine gen_ellipsoid(world, x_size, y_size, z_size)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m g_ellipsoid g_ellipsoid_f.f90
  real*8 :: x_size, y_size, z_size, tempvalue
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) x_size
!f2py intent(in) y_size
!f2py intent(in) z_size

  do x=1, 10
    do y=1, 10
      do z=1, 10
        tempvalue = (x-5.5)**2/x_size**2 + (y-5.5)**2/y_size**2 + (z-5.5)**2/z_size**2
        ! write(*,*) tempvalue
        if (tempvalue <= 1) then
          world(x,y,z) = 1
        end if
      end do
    end do
  end do

end subroutine gen_ellipsoid
