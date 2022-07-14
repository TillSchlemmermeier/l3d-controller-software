subroutine gen_line(world, x1,y1,z1, x2,y2,z2)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m g_shooting_star_f g_shooting_star_f.f90
  real*8 :: x1,y1,z1,x2,y2,z2, tempvalue
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) x1
!f2py intent(in) y1
!f2py intent(in) z1
!f2py intent(in) x2
!f2py intent(in) y2
!f2py intent(in) z2

  do x=1, 10
    do y=1, 10
      do z=1, 10
        tempvalue = sqrt((x-xpos-1)**2+(y-ypos-1)**2+(z-zpos-1)**2)
        world(x,y,z) = 1/(tempvalue+0.0001)**4
      end do
    end do
  end do

end subroutine gen_shooting_star
