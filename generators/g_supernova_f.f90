
subroutine gen_supernova(world, xpos, ypos, zpos)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m g_supernova_f g_supernova_f.f90
  real*8 :: xpos, ypos, zpos, tempvalue
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) xpos
!f2py intent(in) ypos
!f2py intent(in) zpos

  do x=1, 10
    do y=1, 10
      do z=1, 10
        tempvalue = sqrt((x-xpos-1)**2+(y-ypos-1)**2+(z-zpos-1)**2)
        world(x,y,z) = 1/(tempvalue+0.0001)**7
      end do
    end do
  end do

end subroutine gen_supernova
