
subroutine gen_central_glow(world, scale)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m g_central_glow_f g_central_glow_f.f90
  real*8 :: scale, tempvalue
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) scale

  do x=1, 10
    do y=1, 10
      do z=1, 10
        tempvalue = sqrt((x-5-1)**2+(y-5-1)**2+(z-5-1)**2)
        world(x,y,z) = scale * 1/(tempvalue+0.0001)
      end do
    end do
  end do

end subroutine gen_central_glow
