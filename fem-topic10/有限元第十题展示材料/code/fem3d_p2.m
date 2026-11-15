function results = fem3d_p2(outdir)
% FEM3D_P2  Ten-node tetrahedral P2 FEM for -Delta u=f.
% Usage: results = fem3d_p2;
% Method: Note2 pp.11-12; nonhomogeneous lifting: Note1 p.10.
% MATLAB R2016b or later (implicit array expansion); no toolbox required.
% This source has NOT been executed in MATLAB in the delivery environment.
% The independent Python counterpart was executed; see ../data/results.json.
if nargin < 1, outdir = fullfile(fileparts(mfilename('fullpath')),'..','matlab_results'); end
if ~exist(outdir,'dir'), mkdir(outdir); end
poly = run_case(2,'poly',5);
assert(poly.E0 < 1e-10 && poly.E1 < 1e-9,'Polynomial test failed.');
fprintf('Polynomial: E0=%.6e, E1=%.6e, residual=%.6e\n',poly.E0,poly.E1,poly.residual);
ns = [4,8,16]; rows = zeros(3,8);
for k = 1:3
    [s, state] = run_case(ns(k),'sine',5);
    rows(k,:) = [s.n,s.NT,s.NV,s.NE,s.Nfree,s.E0,s.E1,s.residual];
end
results = array2table(rows,'VariableNames',{'n','NT','NV','NE','Nfree','E0','E1','residual'});
disp(results); writetable(results,fullfile(outdir,'sine_results_matlab.csv'));
save(fullfile(outdir,'solution_n16_matlab.mat'),'state','poly','results');
q6 = run_case(4,'sine',6);
fprintf('n=4, m=5 vs 6: rel change E0 %.3e; E1 %.3e\n',...
    abs(q6.E0-rows(1,6))/rows(1,6), abs(q6.E1-rows(1,7))/rows(1,7));
mask = abs(state.coords(:,3)-0.5) < 1e-12;
x = state.coords(mask,1); y = state.coords(mask,2); uh = state.U(mask);
figure; scatter(x,y,22,uh,'filled'); axis equal tight; colorbar;
xlabel('x'); ylabel('y'); title('P2 solution at z=0.5');
saveas(gcf,fullfile(outdir,'slice_z05_matlab.png'));
end

function [s,state] = run_case(n,kind,m)
[node,elem] = cube_mesh(n); NV = size(node,1); NT = size(elem,1);
le = [1 2;1 3;1 4;2 3;2 4;3 4];
allEdge = zeros(NT*6,2);
for k = 1:6, allEdge((k-1)*NT+(1:NT),:) = sort(elem(:,le(k,:)),2); end
[edge,~,idx] = unique(allEdge,'rows');
elem2edge = reshape(idx,NT,6);
elem2dof = [elem,NV+elem2edge];
NE = size(edge,1); Nu = NV+NE;
coords = [node;(node(edge(:,1),:)+node(edge(:,2),:))/2];

% Boundary faces are the sorted triples with multiplicity exactly one.
lf = [1 2 3;1 2 4;1 3 4;2 3 4];
allFace = zeros(NT*4,3);
for k=1:4, allFace((k-1)*NT+(1:NT),:) = sort(elem(:,lf(k,:)),2); end
[face,~,fi] = unique(allFace,'rows');
counts = accumarray(fi,1);
assert(all(counts<=2),'Nonmanifold mesh.');
bdFace = face(counts==1,:);
bdEdge = unique(sort([bdFace(:,[1 2]);bdFace(:,[1 3]);bdFace(:,[2 3])],2),'rows');
[found,be] = ismember(bdEdge,edge,'rows'); assert(all(found));
bd = unique([bdFace(:);NV+be]);
free = setdiff((1:Nu)',bd);

% G(t,:,i) is the physical gradient of barycentric coordinate lambda_i.
v1 = node(elem(:,2),:)-node(elem(:,1),:);
v2 = node(elem(:,3),:)-node(elem(:,1),:);
v3 = node(elem(:,4),:)-node(elem(:,1),:);
detB = dot(v1,cross(v2,v3,2),2); volume = abs(detB)/6;
assert(all(volume>0) && abs(sum(volume)-1)<1e-11);
G = zeros(NT,3,4);
G(:,:,2)=cross(v2,v3,2)./detB;
G(:,:,3)=cross(v3,v1,2)./detB;
G(:,:,4)=cross(v1,v2,2)./detB;
G(:,:,1)=-sum(G(:,:,2:4),3);

% 4-point degree-2 rule; weights sum to one, multiply by physical volume.
a=(5+3*sqrt(5))/20; b=(5-sqrt(5))/20;
lambda=b*ones(4,4); lambda(1:5:16)=a;
localA=zeros(NT,10,10);
for p=1:4
    dp=grad_p2(lambda(p,:),G,le);
    for i=1:10
        for j=1:10
            localA(:,i,j)=localA(:,i,j)+volume.*dot(dp(:,:,i),dp(:,:,j),2)/4;
        end
    end
end
% Accumulate quadrature first; sparse is called outside the quadrature loop.
A=sparse(Nu,Nu);
for i=1:10
    for j=1:10
        A=A+sparse(elem2dof(:,i),elem2dof(:,j),localA(:,i,j),Nu,Nu);
    end
end
[lambda,weight]=duffy_rule(m); bt=zeros(NT,10);
for p=1:numel(weight)
    lam=lambda(p,:); x=zeros(NT,3);
    for k=1:4, x=x+lam(k)*node(elem(:,k),:); end
    [~,~,f]=exact_data(x,kind);
    bt=bt+(weight(p)*volume.*f)*basis_p2(lam,le);
end
rhs=accumarray(elem2dof(:),bt(:),[Nu,1]);

% Dirichlet lift; right-hand correction is essential for polynomial test.
U=zeros(Nu,1); U(bd)=exact_data(coords(bd,:),kind);
b=rhs-A*U;
U(free)=A(free,free)\b(free);
r=A*U-rhs;
residual=norm(r(free))/max(norm(b(free)),eps);

E0=0; E1=0; ue=U(elem2dof);
for p=1:numel(weight)
    lam=lambda(p,:); x=zeros(NT,3);
    for k=1:4, x=x+lam(k)*node(elem(:,k),:); end
    [u,gu]=exact_data(x,kind);
    uh=ue*basis_p2(lam,le)'; gh=zeros(NT,3);
    dp=grad_p2(lam,G,le);
    for k=1:10, gh=gh+ue(:,k).*dp(:,:,k); end
    E0=E0+sum(weight(p)*volume.*(u-uh).^2);
    E1=E1+sum(weight(p)*volume.*sum((gu-gh).^2,2));
end
s=struct('n',n,'NT',NT,'NV',NV,'NE',NE,'Nfree',numel(free),...
    'E0',sqrt(E0),'E1',sqrt(E1),'residual',residual);
state=struct('node',node,'elem',elem,'edge',edge,'elem2dof',elem2dof,...
    'coords',coords,'U',U,'bd',bd);
end

function p=basis_p2(lam,le)
p=[lam.*(2*lam-1),4*lam(le(:,1)).*lam(le(:,2))];
end

function dp=grad_p2(lam,G,le)
dp=zeros(size(G,1),3,10);
for i=1:4, dp(:,:,i)=(4*lam(i)-1)*G(:,:,i); end
for k=1:6
    i=le(k,1); j=le(k,2);
    dp(:,:,4+k)=4*(lam(i)*G(:,:,j)+lam(j)*G(:,:,i));
end
end

function [u,g,f]=exact_data(x,kind)
if strcmp(kind,'poly')
    a=x(:,1); b=x(:,2); c=x(:,3);
    u=a.^2+b.^2+c.^2+a.*b+a.*c+b.*c;
    g=[2*a+b+c,a+2*b+c,a+b+2*c]; f=-6*ones(size(a));
else
    s=sin(pi*x); c=cos(pi*x); u=prod(s,2);
    g=pi*[c(:,1).*s(:,2).*s(:,3),s(:,1).*c(:,2).*s(:,3),s(:,1).*s(:,2).*c(:,3)];
    f=3*pi^2*u;
end
end

function [node,elem]=cube_mesh(n)
% Kuhn triangulation: every cube is divided along monotone coordinate paths.
% Identical global axis ordering makes all shared faces conforming.
[x,y,z]=ndgrid(0:n,0:n,0:n); node=[x(:),y(:),z(:)]/n;
[x,y,z]=ndgrid(0:n-1,0:n-1,0:n-1); base=[x(:),y(:),z(:)];
P=perms(1:3); elem=zeros(6*n^3,4); I=eye(3);
for p=1:6
    steps=[zeros(1,3);cumsum(I(P(p,:),:),1)];
    for k=1:4
        v=base+steps(k,:);
        elem((p-1)*n^3+(1:n^3),k)=1+v(:,1)+(n+1)*v(:,2)+(n+1)^2*v(:,3);
    end
end
end

function [lambda,w]=duffy_rule(m)
% Golub-Welsch Gauss-Legendre on [0,1], followed by the Duffy map.
beta=(1:m-1)./sqrt(4*(1:m-1).^2-1);
[V,D]=eig(diag(beta,1)+diag(beta,-1));
[x,order]=sort(diag(D)); x=(x+1)/2; wg=V(1,order).^2;
lambda=zeros(m^3,4); w=zeros(m^3,1); q=0;
for i=1:m
    for j=1:m
        for k=1:m
            r=x(i); s=x(j); t=x(k); q=q+1;
            xyz=[r,(1-r)*s,(1-r)*(1-s)*t];
            lambda(q,:)=[1-sum(xyz),xyz];
            w(q)=6*wg(i)*wg(j)*wg(k)*(1-r)^2*(1-s);
        end
    end
end
assert(abs(sum(w)-1)<1e-12);
end
