
subroutine world2vox_f(list, world)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m world2vox_fortran world2vox_revis.f90

  real*8, dimension(10,10,10) :: world
  integer, dimension(1000)  :: list
  integer :: x,y,z, index

!f2py intent(out) list
!f2py intent(in) world

  list(:) = 0
  index = 1

  do x=0, 9
    do y=0, 9
      do z=0, 9

        if (mod(z, 2) == 0) then
          if (mod(y, 2) == 0) then
            index = (z*100)+(y*10)+x
          else
            index = (z*100)+(y*10)+9-x
          endif

        else
          if (mod(y, 2) == 0) then
            index = (z*100)+(90-y*10)+9-x
          else
            index = (z*100)+(90-y*10)+x
          endif
        end if

        list(index+1) = int(world(x+1,y+1,z+1)*255)

      end do
    end do
  end do

end subroutine world2vox_f
