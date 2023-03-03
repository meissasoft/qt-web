import React from 'react'

function EnsureClean({goToPage}) {
  return (
    <div className='maindiv background'>
      <div style={{display:"flex" , justifyContent:"center" , alignItems:"center" ,flexDirection :"column" , height:"100%"}}>
        <p style={{ fontSize:"30px" , fontWeight:"500" , marginBottom:"2rem"}}>Are you sure?</p>
<p style={{fontSize:"22px" ,  marginTop:"-18px"}}>FILENAME</p>
<div style={{width:"50%" , display :"flex" ,justifyContent:"space-around" , marginTop:"20px"}} >
    <button className='btn' onClick={()=>goToPage(10)}>
    Yes, I mean it!
    </button>
    <button className='btn' onClick={()=>goToPage(10)}>
    Maybe not...
    </button>
</div>
      </div>
      <button className="footer" onClick={()=>goToPage(0)}> Go To Home</button>
    </div>
  )
}

export default EnsureClean;
