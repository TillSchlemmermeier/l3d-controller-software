all: say_hello world2vox_fortran

say_hello:
	@echo ''
	@echo 'starting make process...'
	@echo ''

world2vox_fortran: world2vox.f90
	@echo 'compiling world2vox...'
	@f2py3 --quiet -c -m world2vox_fortran world2vox_revis.f90
#	@f2py3 --quiet -c -m world2vox_fortran world2vox.f90

clean:
	@echo 'Cleaning up...'
	$(RM) *.so
	$(RM) *.pyc
