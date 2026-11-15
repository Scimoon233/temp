"""3-D tetrahedral P2 FEM; independent, executable counterpart of fem3d_p2.m.

Method: Note2 pp. 11-12 (edge dofs and assembly), Note1 p. 10 (Dirichlet lift).
Only NumPy/SciPy/Matplotlib are required. Run: python fem3d_p2.py
"""
from pathlib import Path
import itertools
import json
import csv
import time
import os
os.environ.setdefault('MPLCONFIGDIR', '/tmp/fem-p2-matplotlib')
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

EDGES = np.array([[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]])
FACES = np.array([[0,1,2],[0,1,3],[0,2,3],[1,2,3]])

def mesh(n):
    ijk = np.array(list(itertools.product(range(n+1), repeat=3)))
    node = ijk / n
    def vid(v):
        return (v[...,0]*(n+1)+v[...,1])*(n+1)+v[...,2]
    cubes = np.array(list(itertools.product(range(n), repeat=3)))
    cells = []
    for perm in itertools.permutations(range(3)):
        steps = np.vstack([np.zeros(3, dtype=int), np.cumsum(np.eye(3, dtype=int)[list(perm)], axis=0)])
        cells.append(vid(cubes[:,None,:] + steps[None,:,:]))
    return node, np.concatenate(cells)

def topology(node, elem):
    nv = len(node)
    edge, inv = np.unique(np.sort(elem[:,EDGES].reshape(-1,2), axis=1), axis=0, return_inverse=True)
    elem2edge = inv.reshape(-1,6)
    dof = np.column_stack([elem, nv+elem2edge])
    faces, count = np.unique(np.sort(elem[:,FACES].reshape(-1,3),axis=1),axis=0,return_counts=True)
    assert count.max() <= 2, 'Nonmanifold mesh'
    boundary_faces = faces[count == 1]
    boundary_edges = np.unique(np.sort(boundary_faces[:,[[0,1],[0,2],[1,2]]].reshape(-1,2),axis=1),axis=0)
    edge_lookup = {tuple(e): i for i,e in enumerate(edge)}
    bd_edge = np.array([edge_lookup[tuple(e)] for e in boundary_edges])
    bd = np.unique(np.r_[boundary_faces.ravel(),nv+bd_edge])
    coords = np.vstack([node,node[edge].mean(axis=1)])
    return edge, dof, bd, coords, boundary_faces

def geometry(node, elem):
    vertices = node[elem]
    B = np.transpose(vertices[:,1:,:]-vertices[:,:1,:],(0,2,1))
    invB = np.linalg.inv(B)
    vol = np.abs(np.linalg.det(B))/6
    G = np.concatenate([-invB.sum(axis=1,keepdims=True),invB],axis=1)
    return vertices, vol, G

def phi(lam):
    return np.r_[lam*(2*lam-1),4*lam[EDGES[:,0]]*lam[EDGES[:,1]]]

def dphi(lam, G):
    v = G*(4*lam-1)[None,:,None]
    e = 4*(lam[EDGES[:,0]][None,:,None]*G[:,EDGES[:,1],:] + lam[EDGES[:,1]][None,:,None]*G[:,EDGES[:,0],:])
    return np.concatenate([v,e],axis=1)

def quadrature(m=5):
    # Duffy map from [0,1]^3: xi=r, eta=(1-r)s, zeta=(1-r)(1-s)t.
    # Jacobian=(1-r)^2(1-s). Multiplying weights by 6 gives sum(w)=1.
    x,w = leggauss(m); x=(x+1)/2; w=w/2
    result=[]
    for i,j,k in itertools.product(range(m),repeat=3):
        r,s,t=x[i],x[j],x[k]
        xyz=np.array([r,(1-r)*s,(1-r)*(1-s)*t])
        result.append((np.r_[1-xyz.sum(),xyz],6*w[i]*w[j]*w[k]*(1-r)**2*(1-s)))
    return result

def exact(x, kind):
    if kind == 'poly':
        a,b,c=x.T
        u=a*a+b*b+c*c+a*b+a*c+b*c
        grad=np.column_stack([2*a+b+c,a+2*b+c,a+b+2*c])
        return u, grad, np.full(len(x),-6.)
    s=np.sin(np.pi*x); c=np.cos(np.pi*x)
    u=s.prod(axis=1)
    grad=np.pi*np.column_stack([c[:,0]*s[:,1]*s[:,2],s[:,0]*c[:,1]*s[:,2],s[:,0]*s[:,1]*c[:,2]])
    return u, grad, 3*np.pi**2*u

def solve(n, kind='sine', m=5):
    start=time.perf_counter()
    node,elem=mesh(n)
    edge,dof,bd,coords,bd_faces=topology(node,elem)
    vertices,vol,G=geometry(node,elem)
    nt=len(elem); nd=len(coords)
    assert abs(vol.sum()-1)<1e-12
    # Positive symmetric 4-point tetrahedral rule; degree 2 exact, weights sum to 1.
    a=(5+3*np.sqrt(5))/20; b=(5-np.sqrt(5))/20
    aq=np.full((4,4),b); np.fill_diagonal(aq,a)
    local=np.zeros((nt,10,10))
    for lam in aq:
        dp=dphi(lam,G)
        local+=vol[:,None,None]*np.einsum('tij,tkj->tik',dp,dp)/4
    rows=np.repeat(dof,10,axis=1).ravel()
    cols=np.tile(dof,(1,10)).ravel()
    A=coo_matrix((local.ravel(),(rows,cols)),shape=(nd,nd)).tocsr()
    local_b=np.zeros((nt,10))
    for lam,w in quadrature(m):
        x=np.einsum('i,tij->tj',lam,vertices)
        f=exact(x,kind)[2]
        local_b+=(vol*w*f)[:,None]*phi(lam)[None,:]
    rhs=np.bincount(dof.ravel(),weights=local_b.ravel(),minlength=nd)
    U=np.zeros(nd); U[bd]=exact(coords[bd],kind)[0]
    free=np.setdiff1d(np.arange(nd),bd)
    lifted=rhs-A@U
    Aff=A[free][:,free]
    U[free]=spsolve(Aff,lifted[free])
    residual=np.linalg.norm((A@U-rhs)[free])/max(np.linalg.norm(lifted[free]),np.finfo(float).eps)
    E0=0.; E1=0.
    ue=U[dof]
    for lam,w in quadrature(m):
        x=np.einsum('i,tij->tj',lam,vertices)
        u,grad,_=exact(x,kind)
        uh=ue@phi(lam)
        gh=np.einsum('ti,tij->tj',ue,dphi(lam,G))
        E0+=np.dot(vol*w,(u-uh)**2)
        E1+=np.dot(vol*w,np.sum((grad-gh)**2,axis=1))
    row={'n':n,'NT':nt,'NV':len(node),'NE':len(edge),'Ndof':nd,'Nfree':len(free),
         'E0':float(np.sqrt(E0)),'E1':float(np.sqrt(E1)),'residual':float(residual),
         'max_nodal_error':float(np.max(np.abs(U-exact(coords,kind)[0]))),
         'seconds':time.perf_counter()-start}
    return row,{'node':node,'elem':elem,'edge':edge,'dof':dof,'coords':coords,'U':U,'bd':bd,'bd_faces':bd_faces,'A':A}

def local_checks():
    nodes=np.vstack([np.eye(4),np.array([(np.eye(4)[i]+np.eye(4)[j])/2 for i,j in EDGES])])
    dual=np.stack([phi(lam) for lam in nodes])
    v=np.array([[[.1,.2,-.3],[1.2,.1,.2],[.4,1.4,.1],[-.1,.5,1.3]]])
    B=(v[0,1:]-v[0,0]).T
    inv=np.linalg.inv(B)
    G=np.concatenate([-inv.sum(axis=0)[None,:],inv],axis=0)[None,:,:]
    lam=np.array([.13,.21,.29,.37])
    dp=dphi(lam,G)[0]
    # At barycenter, 10 gradients are sampled as vectors in R^3, so rank <= 3.
    Dc=dphi(np.ones(4)/4,G)[0]
    q=quadrature(5)
    import math
    max_moment=0.
    for powers in itertools.product(range(3),repeat=4):
        if sum(powers)>2: continue
        val=sum(w*np.prod(l**powers) for l,w in q)
        ref=6*np.prod([math.factorial(k) for k in powers])/math.factorial(3+sum(powers))
        max_moment=max(max_moment,abs(val-ref))
    a=(5+3*np.sqrt(5))/20; b=(5-np.sqrt(5))/20
    aq=np.full((4,4),b); np.fill_diagonal(aq,a)
    K=sum(dphi(l,G)[0]@dphi(l,G)[0].T/4 for l in aq)
    return {'nodal_duality_max':float(abs(dual-np.eye(10)).max()),
            'partition_error':float(abs(phi(lam).sum()-1)),
            'gradient_sum_error':float(abs(dp.sum(axis=0)).max()),
            'duffy_weight_sum':float(sum(w for _,w in q)),
            'degree2_moment_error':float(max_moment),
            'stiffness_rank_4point':int(np.linalg.matrix_rank(K,tol=1e-10)),
            'stiffness_rank_centroid':int(np.linalg.matrix_rank(Dc@Dc.T,tol=1e-10))}

def main():
    out=Path(__file__).resolve().parent.parent/'data';out.mkdir(exist_ok=True)
    checks=local_checks()
    assert checks['nodal_duality_max']<1e-13
    assert checks['stiffness_rank_4point']==9
    assert checks['stiffness_rank_centroid']<=3
    print('local checks:',checks,flush=True)
    poly,state_poly=solve(2,'poly')
    assert poly['E0']<1e-11 and poly['E1']<1e-10
    print('polynomial:',poly,flush=True)
    rows=[]
    for n in [4,8,16]:
        row,state=solve(n)
        rows.append(row);print('sine:',row,flush=True)
    check6,_=solve(4,m=6)
    qcheck={k:abs(check6[k]-rows[0][k])/rows[0][k] for k in ['E0','E1']}
    for a,b in zip(rows,rows[1:]):
        assert b['E0']<a['E0'] and b['E1']<a['E1']
    assert max(qcheck.values())<1e-5
    result={'runtime':'Python / NumPy / SciPy; MATLAB source supplied separately',
            'mesh':'6 Kuhn tetrahedra per cube; global axis ordering; h=sqrt(3)/n',
            'quadrature':'stiffness: degree-2 4-point rule; load/errors: 5x5x5 Duffy-Gauss, sum(w)=1',
            'checks':checks,'polynomial':poly,'sine':rows,'quadrature_check_m5_vs_m6_n4':qcheck}
    (out/'results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    with (out/'sine_results.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    np.savez_compressed(out/'solution_n16.npz',**{k:v for k,v in state.items() if k!='A'})
    # All P2 nodes on z=.5 are a (2n+1)^2 tensor grid on this mesh.
    mask=abs(state['coords'][:,2]-.5)<1e-12
    xy=state['coords'][mask,:2];z=state['U'][mask]
    np.savetxt(out/'slice_z05.csv',np.column_stack([xy,z,np.sin(np.pi*xy[:,0])*np.sin(np.pi*xy[:,1])]),delimiter=',',header='x,y,uh,u_exact',comments='')
    print('quadrature sensitivity:',qcheck,flush=True)
    print('saved:',out,flush=True)

if __name__=='__main__':
    main()
