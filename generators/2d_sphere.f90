
subroutine sphere2d(world, xpos, ypos, fade)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m sphere2d 2d_sphere.f90
  real*8 :: xpos, ypos, tempvalue, fade
  real*8, dimension(20,10) :: world
  integer :: x,y

!f2py intent(out) world
!f2py intent(in) xpos
!f2py intent(in) ypos
!f2py intent(in) fade

  do x=1, 20
    do y=1, 10
      tempvalue = sqrt((x-xpos-1)**2+(y-ypos-1)**2)
        world(x,y) = 1/(tempvalue+0.0001)**fade
    end do
  end do

end subroutine sphere2d
