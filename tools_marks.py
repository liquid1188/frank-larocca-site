# One source for every chant mark on the site. Puncta are pen-drawn: slightly rounded ends, a gentle bow on top and bottom.
import re, cairosvg
from PIL import Image
RED='#b7342c'; GOLD='#c9a656'; VELLUM='#ece3cf'; NAVY='#15121c'
PY={'j':10,'i':15,'h':20,'g':25,'f':30,'e':35,'d':40}
W,Hh=7.2,6.2
GRAD='<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2c37a"/><stop offset=".55" stop-color="#c9a656"/><stop offset="1" stop-color="#9a7c36"/></linearGradient></defs>'
def punctum(x,y,w=W,h=Hh):
    b=0.28; r=0.45  # bow and corner softening
    return (f'M{x+r:.2f},{y+b:.2f} Q{x+w/2:.2f},{y-b:.2f} {x+w-r:.2f},{y+b:.2f} '
            f'Q{x+w:.2f},{y+b:.2f} {x+w:.2f},{y+b+r:.2f} L{x+w:.2f},{y+h-b-r:.2f} Q{x+w:.2f},{y+h-b:.2f} {x+w-r:.2f},{y+h-b:.2f} '
            f'Q{x+w/2:.2f},{y+h+b:.2f} {x+r:.2f},{y+h-b:.2f} Q{x:.2f},{y+h-b:.2f} {x:.2f},{y+h-b-r:.2f} L{x:.2f},{y+b+r:.2f} Q{x:.2f},{y+b:.2f} {x+r:.2f},{y+b:.2f} Z')
def sq(x,p,hollow=False,py=PY,w=W,h=Hh):
    y=py[p]-h/2
    if hollow: return f'<path d="{punctum(x+0.6,y+0.6,w-1.2,h-1.2)}" fill="none" stroke="FILL" stroke-width="1.3"/>'
    return f'<path d="{punctum(x,y,w,h)}"/>'
def stem(x,p1,p2,py=PY,h=Hh):
    top=min(py[p1],py[p2])-h/2+0.3; bot=max(py[p1],py[p2])+h/2-0.3
    return f'<rect x="{x:.1f}" y="{top:.1f}" width="1.3" height="{bot-top:.1f}"/>'
def flat(x,p,py=PY):
    y=py[p]; return f'<rect x="{x:.1f}" y="{y-7:.1f}" width="1.2" height="10"/><path d="M{x+1.2:.1f} {y-1.5:.1f} q4 -2.5 4 1 q0 3 -4 3.5z"/>'
def clef(x,ly=10): return f'<rect x="{x}" y="{ly-6}" width="1.4" height="12"/><rect x="{x+2.4}" y="{ly-6}" width="5" height="4.8"/><rect x="{x+2.4}" y="{ly+1.2}" width="5" height="4.8"/>'
def dot(x,p,py=PY): return f'<circle cx="{x+W+2.2:.1f}" cy="{py[p]-3.6:.1f}" r="1.1"/>'
def render(neumes, gid, clef_line=10):
    x=3; out=[clef(x,clef_line)]; x+=13
    for kind,ps in neumes:
        if kind=='pes': out+=[sq(x,ps[0]),sq(x,ps[1]),stem(x,ps[0],ps[1])]; x+=W+8
        elif kind=='clivis': out+=[stem(x,ps[0],ps[1]),sq(x+1.3,ps[0]),sq(x+1.3+W,ps[1])]; x+=2*W+10
        elif kind=='flat': out+=[flat(x,ps[0]),sq(x+7,ps[0])]; x+=W+14
        elif kind=='hollow': out.append(sq(x,ps[0],True)); x+=W+6
        elif kind=='dot': out+=[sq(x,ps[0]),dot(x,ps[0])]; x+=W+9
        else: out.append(sq(x,ps[0])); x+=W+6
    width=x+2
    lines=''.join(f'<line x1="0" y1="{y}" x2="{width:.0f}" y2="{y}"/>' for y in (10,20,30,40))
    body=''.join(out).replace('FILL',f'url(#{gid})')
    return f'<svg viewBox="0 0 {width:.0f} 50" aria-hidden="true" focusable="false">{GRAD.format(gid=gid)}<g stroke="{RED}" stroke-width="1.8">{lines}</g><g fill="url(#{gid})">{body}</g></svg>', width
# Psalm 50, Tone I: Mi(f) se(gh) ré(h) re(h) me(i♭) i(h°) De(h g) us(h° h.)
SHORT=[('p','f'),('pes','gh'),('p','h'),('p','h'),('flat','i'),('hollow','h'),('p','h')]
FULL=SHORT+[('p','g'),('hollow','h'),('dot','h')]
def build():
    svg,w=render(SHORT,'gilt'); open('src/_includes/mark.njk','w').write(svg+'\n')
    svg2,w2=render(FULL,'gilt2'); open('src/_includes/mark-wide.njk','w').write(svg2+'\n')
    # divider: intonation Mi-se-ré at divider scale (lines 8 apart)
    pyd={'h':9,'g':13,'f':17}; wd,hd=6.0,5.4
    x=1; d=[sq(x,'f',py=pyd,w=wd,h=hd)]; x+=wd+6; d+=[sq(x,'g',py=pyd,w=wd,h=hd),sq(x,'h',py=pyd,w=wd,h=hd),stem(x,'g','h',py=pyd,h=hd)]; x+=wd+7; d.append(sq(x,'h',py=pyd,w=wd,h=hd)); x+=wd+1
    open('src/_includes/staff-rule.njk','w').write(f'<div class="staff" aria-hidden="true"><svg class="staff-neumes" viewBox="0 -4 {x+1:.0f} 30" width="{x+1:.0f}" height="30" aria-hidden="true"><g fill="{GOLD}">{"".join(d)}</g></svg></div>\n')
    # favicon: intonation
    fb=(sq(10,'f')+sq(24,'g')+sq(24,'h')+stem(24,'g','h')+sq(40,'h')).replace('FILL',GOLD)
    fav=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="{NAVY}"/><g transform="translate(0 7)"><g stroke="{RED}" stroke-width="2"><line x1="6" y1="10" x2="58" y2="10"/><line x1="6" y1="20" x2="58" y2="20"/><line x1="6" y1="30" x2="58" y2="30"/><line x1="6" y1="40" x2="58" y2="40"/></g><g fill="{GOLD}">{fb}</g></g></svg>'
    open('src/assets/favicon.svg','w').write(fav+'\n')
    for s in (32,180): cairosvg.svg2png(url='src/assets/favicon.svg', write_to=f'src/assets/favicon-{s}.png', output_width=s, output_height=s)
    # Lumen Verum: c3 clef, LU(h) MEN(g)
    def lvm(red,gold,text,w=150):
        lines=''.join(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}"/>' for y in (10,20,30,40))
        cx=w/2-18; notes=(clef(cx,20)+sq(cx+15,'h')+sq(cx+27,'g')).replace('FILL',gold)
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 84"><g stroke="{red}" stroke-width="1.8">{lines}</g><g fill="{gold}">{notes}</g>
<text x="{w/2:.0f}" y="63" text-anchor="middle" font-family="Cormorant Garamond, Garamond, Georgia, serif" font-size="14" letter-spacing="1.8" fill="{text}">LUMEN VERUM</text>
<text x="{w/2:.0f}" y="76" text-anchor="middle" font-family="Alegreya, Georgia, serif" font-size="7.5" letter-spacing="3" fill="{gold}">MUSIC</text></svg>'''
    open('src/images/affil/lumen-verum-music.svg','w').write(lvm(RED,GOLD,VELLUM))
    open('/mnt/user-data/outputs/lumen-verum-music-dark.svg','w').write(lvm(RED,GOLD,VELLUM))
    open('/mnt/user-data/outputs/lumen-verum-music-light.svg','w').write(lvm(RED,'#8a6d2f','#221d2b'))
    # press kit lockups
    def inner(svg):
        vb=re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"',svg); w,h=float(vb.group(1)),float(vb.group(2))
        body=re.sub(r'^<svg[^>]*>','',svg); body=re.sub(r'</svg>$','',body); return body,w,h
    def stacked():
        b,w,h=inner(svg2); scale=5.2; sw=w*scale; sh=h*scale; Wc,Hc=1600,1000; x0=(Wc-sw)/2; y0=110
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}"><rect width="{Wc}" height="{Hc}" fill="{NAVY}"/>
<g transform="translate({x0:.1f} {y0}) scale({scale})">{b}</g>
<text x="{Wc/2}" y="{y0+sh+165}" text-anchor="middle" font-family="Cormorant Garamond" font-weight="500" font-size="150" fill="{VELLUM}">Frank La Rocca</text>
<line x1="{x0:.0f}" y1="{y0+sh+225}" x2="{x0+sw:.0f}" y2="{y0+sh+225}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="2"/>
<rect x="{Wc/2-10}" y="{y0+sh+215}" width="20" height="20" fill="{GOLD}" transform="rotate(45 {Wc/2} {y0+sh+225})"/>
<text x="{Wc/2}" y="{y0+sh+300}" text-anchor="middle" font-family="Alegreya" font-size="38" letter-spacing="12" fill="{GOLD}">COMPOSER OF SACRED MUSIC</text></svg>'''
    def horizontal():
        b,w,h=inner(svg); scale=3.2; sw=w*scale; sh=h*scale; Wc,Hc=1800,700; total=sw+140+740; x0=(Wc-total)/2; y0=(Hc-sh)/2
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}"><rect width="{Wc}" height="{Hc}" fill="{NAVY}"/>
<g transform="translate({x0:.1f} {y0:.1f}) scale({scale})">{b}</g>
<line x1="{x0+sw+70:.0f}" y1="{Hc/2-100}" x2="{x0+sw+70:.0f}" y2="{Hc/2+100}" stroke="{GOLD}" stroke-width="2.5"/>
<text x="{x0+sw+140:.0f}" y="{Hc/2+34}" font-family="Cormorant Garamond" font-weight="500" font-size="100" fill="{VELLUM}">Frank La Rocca</text></svg>'''
    def mark_alone():
        b,w,h=inner(svg); scale=10; sw=w*scale; sh=h*scale; Wc,Hc=1600,900
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}"><rect width="{Wc}" height="{Hc}" fill="{NAVY}"/><g transform="translate({(Wc-sw)/2:.1f} {(Hc-sh)/2:.1f}) scale({scale})">{b}</g></svg>'''
    return stacked(), horizontal(), mark_alone()
if __name__=='__main__':
    import sys
    tag=sys.argv[1] if len(sys.argv)>1 else 'v4'
    st,ho,ma=build()
    for name,svgtxt in [('lockup-stacked',st),('lockup-horizontal',ho),('mark',ma)]:
        png=f'/tmp/{name}.png'; cairosvg.svg2png(bytestring=svgtxt.encode(), write_to=png)
        Image.open(png).convert('RGB').save(f'src/images/brand/frank-la-rocca-{name}-{tag}.jpg', quality=94)
        open(f'/mnt/user-data/outputs/frank-la-rocca-{name}.svg','w').write(svgtxt)
    print('built', tag)
