all: say_hello world2vox_fortran

say_hello:
	@echo ''
	@echo 'starting make process...'
	@echo ''

world2vox_fortran: world2vox.f90
	@echo 'compiling world2vox...'
	@f2py3 --quiet -c -m world2vox_fortran world2vox_revis.f90
#	@f2py3 --quiet -c -m world2vox_fortran world2vox.f90

g_genhsphere:
	@f2py3 -c -m generators/g_genhsphere generators/g_growing_sphere_f.f90

clean:
	@echo 'Cleaning up...'
	$(RM) *.so
	$(RM) *.pyc
	$(RM) generators/*.so
	$(RM) generators/*.pyc
	$(RM) effects/*.so
	$(RM) effects/*.pyc
