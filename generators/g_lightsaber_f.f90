subroutine gen_lightsaber(world, pout, point)

  implicit none

! Now comes the variables declaration
  integer, dimension(3) :: pout, point, p3, cross_product
  real*8, dimension(10,10,10) :: world
  integer :: x,y,z

!f2py intent(out) world
!f2py intent(in) pout
!f2py intent(in) point

FUNCTION cross(a, b)
  INTEGER, DIMENSION(3) :: cross
  INTEGER, DIMENSION(3), INTENT(IN) :: a, b

  cross(1) = a(2) * b(3) - a(3) * b(2)
  cross(2) = a(3) * b(1) - a(1) * b(3)
  cross(3) = a(1) * b(2) - a(2) * b(1)
END FUNCTION cross


  do x=1, 10
    do y=1, 10
      do z=1, 10
        p3 = (x,y,z)
        cross_product = cross(point - pout, p3 - pout)
        d = NORM2(cross_product)/(NORM2(point-pout)+0.01)
        world(x,y,z) = 0.5 * (1/(d+0.0001)**8
      end do
    end do
  end do

end subroutine gen_lightsaber
