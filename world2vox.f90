
subroutine world2vox_f(world)

  implicit none

! Now comes the variables declaration
! compile with f2py3 -c -m world2vox_f world2vox.f90

  real*8, dimension(10,10,10) :: world
  integer, dimension(1000,2)  :: list
  integer :: x,y,z, index

!f2py intent(in) world
!f2py intent(out) list

  index = 0

  do x=1, 10
    do y=1, 10
      do z=1, 10
        if (mod(z, 2) == 0) then
          if (mod(y, 2) == 0) then
            list(index, 1) = (z*100)+(y*10)+x
          else
            list(index, 1) = (z*100)+(y*10)+9-x
          endif
        else
          if (mod(y, 2) == 0) then
            list(index, 1) = (z*100)+(90-y*10)+x
          else
            list(index, 1) = (z*100)+(90-y*10)+9-x
          endif
        end if

        list(index, 2) = int(world(x,y,z)*255)
        index = index + 1

      end do
    end do
  end do

end subroutine world2vox_f
