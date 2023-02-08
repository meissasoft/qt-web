import React from 'react'
import "./components.css";
function Reference({goToPage}) {
  return (
    <div className='maindiv'>
      <div style={{display:"flex" , justifyContent:"center" , alignItems:"center" ,flexDirection :"column" , height:"100%"}}>
        <h1 style={{ fontSize:"30px" , fontWeight:"500"}}>Is the pipetrain solvent-cleaned</h1>
        <p >and full of air?</p>
<p style={{fontSize:"20px" , }}>A reference signal needs to be obtained and these <br/>

conditions must be met</p>
<div style={{width:"60%" , display :"flex" ,justifyContent:"space-around" , marginTop:"20px"}} >
    <button className='btn'onClick={()=>goToPage(6)}>
    Yep, get a reference!
    </button>
    <button className='btn' onClick={()=>goToPage(6)}>
    Nope, use old reference
    </button>
</div>
      </div>
    </div>
  )
}

export default Reference;
