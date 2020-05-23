
subroutine gen_torus(world, n, thickness, xpos, ypos, zpos)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m g_genhsphere g_growing_sphere_f.f90
  real*8 :: thickness, distance
  real*8, dimension(25) :: xpos, ypos, zpos
  real*8, dimension(10,10,10) :: world
  integer :: x, y, z, n, i

!f2py intent(out) world
!f2py intent(in) n
!f2py intent(in) thickness
!f2py intent(in) xpos
!f2py intent(in) ypos
!f2py intent(in) zpos

  do i=1, n
    do x=1, 10
      do y=1, 10
        do z=1, 10
          distance = sqrt((x-xpos(i)-5.5)**2+(y-ypos(i)-1)**2+(z-zpos(i)-5.5)**2)
          if (distance < thickness) then
            world(x,y,z) = 1
          end if
        end do
      end do
    end do
  end do

end subroutine gen_torus
