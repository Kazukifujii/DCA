PROGRAM TEST1
  !IMPLICIT none
  !INCLUDE 'mpif.h'
  !CALL MPI_Init(ierr)
  !CALL MPI_Comm_size(MPI_COMM_WORLD, Nproc, ierr)
  !CALL MPI_Comm_rank(MPI_COMM_WORLD, Nid, ierr)
  !IF(Nid.EQ.0) WRITE(*,*) ' Nproc = ',Nproc
  implicit none
  integer:: natom,i,j,nx,nxx,ix,irr
  real(8):: a,b,c,rmin,rmax,xx(3),pp(3)
  real(8),allocatable:: pos(:,:),dist(:,:)
  character(8)::strn
  ! a=5.d0
  ! b=7.d0
  ! c=8.d0
  ! natom=6
  ! rmin=2.8
  ! rmax=3.2
  if(iargc()/=6) stop 'supply a b c rmin rmax natom'
  call getarg(1,strn);  read(strn,*) a
  call getarg(2,strn);  read(strn,*) b
  call getarg(3,strn);  read(strn,*) c
  call getarg(4,strn);  read(strn,*) rmin
  call getarg(5,strn);  read(strn,*) rmax
  call getarg(6,strn);  read(strn,*) natom
  !write(6,*)a,b,c,rmin,rmax,natom
  !stop
  allocate(pos(3,natom),dist(natom,natom)) !fractional
  do 
     call randzeolite(a,b,c,rmin,rmax,natom,pos,irr)
     if(irr==1) cycle
     do i=1,natom
        do j=1,natom
           pp = pos(:,j)-pos(:,i) + 2d0  ! fractional, integer offset 2d0 to make this positive
           dist(i,j) = sum( ((pp-nint(pp))*[a,b,c])**2 )**0.5
        enddo
     enddo
     do j=1,natom
        nx=0
        do i=1,natom
           if(dist(i,j)<rmax)nx=nx+1
        enddo
        if(nx-1/=4) goto 999
     enddo
     exit
999  continue
  enddo   
!!!!!!!!!!!!!!!!!!!!!!!!!!
  write(6,"('Zeolite random: Ortho a b c, rmin rmax')")
  write(6,"('rmin rmax=',3f12.6,'  ',2f9.3)")a,b,c, rmin,rmax
  do i=1,natom
     write(*,"(3f12.6,i5,' !pos cartsian')")pos(1:3,i)*[a,b,c],i
  enddo
  do j=1,natom
     do i=1,natom
        if(i==j) cycle
        if(dist(i,j)<rmax) then
           write(6,"(2i4,' !pair index')")j,i
           nx=nx+1
        endif   
     enddo
  enddo
  write(6,"('--- distance matrix ---')")
  do j=1,natom
     write(*,"(100f6.2)",advance='no') (dist(i,j),i=1,natom)
     nx=0
     do i=1,natom
        if(dist(i,j)<rmax) then
           nx=nx+1
        endif   
     enddo
     nxx=0
     do i=1,natom
        if(dist(i,j)<rmin)nxx=nxx+1
     enddo
     write(*,"(3i5,a)") nx-1, nxx-1,j,' !nx, distance from '
  enddo
  !CALL MPI_Finalize(ierr)
END PROGRAM TEST1

subroutine randzeolite(a,b,c,rmin,rmax,natom,pos,irr)
  implicit none
  integer:: natom,i,j,inum,irand,ic,nat,nbondmx,nbond(natom),irr
  real(8):: a,b,c,rmin,rmax,xx(3),pos(3,natom),pp(3),dist,posn(3)
  real(8),parameter:: pi=atan(1d0)*4d0,pi2=pi*2d0
  pos(:,1)=[0d0,0d0,0d0] !first atom
  ic=1
  nat=1
  nbondmx=4
  irr=0
  do
     nbond=0
     do i=1,nat !bond number = bond(i), i=1,nat
        do j=1,nat
           if(i==j) cycle
           pp = (pos(:,j)-pos(:,i))+2d0  ! fractional, integer offset 2d0 to make this positive
           dist = sum( ((pp-nint(pp))*[a,b,c])**2 )**0.5
           !write(*,*)'ijdist',i,j,dist
           if(dist<rmax) nbond(i) = nbond(i)+1
        enddo
     enddo
     do i=1,nat
        if(nbond(i)>nbondmx) then
           irr=1 !stop 'nbond(i)>nbondmx somehting wrong. check algorithm'
           return
        endif
     enddo   
     !write(6,*)'xxx111',ic,nat,'xxx',(nbond(i),i=1,nat)
     if(nbond(ic)==nbondmx) then
        ic=ic+1
        if(ic>nat) then
           irr=1
           return !stop 'ic>nat somthing wrong'
        endif
        cycle
     endif
     call randompos(a,b,c,rmin,rmax,pos,nat,ic,nbond,nbondmx, posn) !new position surrounding ic
     nat=nat+1
     pos(:,nat)=posn
     !write(*,"(3f9.4,2i5,' !xxx222 pos')")pos(1:3,i)*[a,b,c],nat,ic
     if(nat==natom) return
  enddo
endsubroutine randzeolite

subroutine randompos(a,b,c,rmin,rmax,pos,natom,ic,nbond,nbondmx, posn) !pos ,posn fractonal
  implicit none
  integer::natom,ic,i,nbondmx
  real(8),parameter:: pi=atan(1d0)*4d0,pi2=pi*2d0
  real(8)::xx(3),a,b,c,rmin,rmax,pos(3,natom),posn(3),theta,phi,poss(3),dist,pos0(3),pp(3),r
  integer:: nbond(natom),imax
  pos0=pos(:,ic) !center
  imax=0
  do
     imax=imax+1
     call random_number(xx) !three random numbers [0,1].
     r = xx(1)*(rmax-rmin)+ rmin !r is between rmin rmax
     theta = xx(2)*pi
     phi   = xx(3)*pi2
     poss= pos0*[a,b,c] + r*[sin(phi)*cos(theta),sin(phi)*sin(theta),cos(phi)]
     !print *,'rrrrr=',r
     poss= poss*[1d0/a,1d0/b,1d0/c] + [2d0,2d0,2d0] !poss in fractional
     poss= poss - [(int(poss(i)),i=1,3)] 
     do i=1,natom 
        pp = poss - pos(:,i) ! fractional
        dist = sum( ((pp-nint(pp))*[a,b,c])**2 )**0.5
        if(dist<rmin) goto 8888 !more than four bond for i. restart
        if(dist<rmax .and. nbond(i)+1 > nbondmx) goto 8888 !more than four bond for i. restart
     enddo
     posn=poss
     exit
8888 continue
     !write(6,*)imax
     if(imax>100000) stop 'too many imax'
  enddo
end subroutine randompos
