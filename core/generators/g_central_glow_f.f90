
subroutine gen_central_glow(world, scale, xpos, ypos, zpos)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m gen_central_glow_f g_central_glow_f.f90
  real*8 :: scale, tempvalue, xpos, ypos, zpos
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) scale
!f2py intent(in) xpos
!f2py intent(in) ypos
!f2py intent(in) zpos

  if(scale <= 0) then
    scale = scale + 0.01
  end if

  do x=1, 10
    do y=1, 10
      do z=1, 10
        tempvalue = sqrt(real((x-xpos)**2+(y-ypos)**2+(z-zpos)**2))
        world(x,y,z) = 1/(tempvalue+0.0001)**scale
      end do
    end do
  end do

end subroutine gen_central_glow
