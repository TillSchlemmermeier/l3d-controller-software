
subroutine circle2d(world, s_size, xpos, ypos)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m circle2d 2d_circle.f90
  real*8 :: s_size, xpos, ypos, tempvalue
  real*8, dimension(60, 10) :: world
  integer :: x,y

!f2py intent(out) world
!f2py intent(in) s_size
!f2py intent(in) xpos
!f2py intent(in) ypos

  do x=1, 60
    do y=1, 10
      tempvalue = sqrt((x-xpos-1)**2+(y-ypos-1)**2)
      world(x,y) = 1/abs((s_size-tempvalue+0.0001))**4
    end do
  end do

end subroutine circle2d
