
subroutine gen_sphere(world, s_size, xpos, ypos, zpos)

  implicit none

! Now comes the variables declaration
! compile with f2py -c -m g_sphere_f_helper g_sphere_f.f90
  real*8 :: s_size, xpos, ypos, zpos, tempvalue
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) s_size
!f2py intent(in) xpos
!f2py intent(in) ypos
!f2py intent(in) zpos

  do x=1, 10
    do y=1, 10
      do z=1, 10
        tempvalue = sqrt((x-xpos)**2+(y-ypos)**2+(z-zpos)**2)
        if (tempvalue <= s_size) then
          world(x,y,z) = 1.0D0
        else
          world(x,y,z) = 0.0D0
        end if     
      end do
    end do
  end do

end subroutine gen_sphere

