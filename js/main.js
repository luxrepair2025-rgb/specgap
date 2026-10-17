(function(){
  var CHANNEL=document.documentElement.dataset.channel;
  var btn=document.querySelector('.menu-btn'),ul=document.querySelector('nav ul');
  if(btn)btn.addEventListener('click',function(){var o=ul.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
  var y=document.getElementById('year');if(y)y.textContent=new Date().getFullYear();
  var vids=(window.SPECGAP_VIDEOS||[]).slice().sort(function(a,b){return b.date.localeCompare(a.date)});
  function esc(s){return String(s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
  function fmt(d){return new Date(d+'T12:00:00').toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'})}
  function card(v){return '<article class="card video"><a href="https://www.youtube.com/watch?v='+encodeURIComponent(v.id)+'" target="_blank" rel="noopener" aria-label="Watch on YouTube: '+esc(v.title)+' (opens in a new tab)">'+
    '<div class="thumb"><img src="https://i.ytimg.com/vi/'+encodeURIComponent(v.id)+'/hqdefault.jpg" alt="Thumbnail for '+esc(v.title)+'" loading="lazy" decoding="async" width="480" height="360"><div class="play" aria-hidden="true"><span></span></div></div>'+
    '<div class="body"><div class="meta"><span class="tag">'+esc(v.category)+'</span><time datetime="'+esc(v.date)+'">'+fmt(v.date)+'</time></div><h3>'+esc(v.title)+'</h3><p>'+esc(v.description)+'</p></div></a></article>'}
  function render(el,list){el.innerHTML=list.length?list.map(card).join(''):'<p class="empty">No videos in this category yet. Check back soon.</p>'}
  var latest=document.getElementById('latest-videos');if(latest&&vids.length)render(latest,vids.slice(0,3));
  var feat=document.getElementById('featured-videos');if(feat&&vids.length)render(feat,vids.filter(function(v){return v.featured}).slice(0,3));
  var all=document.getElementById('all-videos'),f=document.getElementById('filters');
  if(all&&vids.length){f.hidden=false;all.className='grid';
    var cats=['All'].concat(vids.map(function(v){return v.category}).filter(function(c,i,a){return a.indexOf(c)===i}));
    var cur=new URLSearchParams(location.search).get('category')||'All';if(cats.indexOf(cur)<0)cur='All';
    function go(c){cur=c;render(all,c==='All'?vids:vids.filter(function(v){return v.category===c}));
      f.querySelectorAll('button').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.cat===c)});
      document.getElementById('count').textContent=all.querySelectorAll('.video').length+' video(s)';}
    f.innerHTML=cats.map(function(c){return '<button type="button" data-cat="'+esc(c)+'" aria-pressed="false">'+esc(c)+'</button>'}).join('');
    f.addEventListener('click',function(e){var b=e.target.closest('button');if(b){go(b.dataset.cat);history.replaceState(null,'',b.dataset.cat==='All'?location.pathname:'?category='+encodeURIComponent(b.dataset.cat))}});
    go(cur);
  }
})();
