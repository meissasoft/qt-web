import React from 'react'

function Sure() {
  return (
    <div className='maindiv'>
    <div style={{display:"flex" , justifyContent:"center" , alignItems:"center" ,flexDirection :"column" , height:"100%"}}>
      <p style={{ fontSize:"30px" , fontWeight:"500" , marginBottom:"2rem"}}>Do You Want to Stop Collecting </p>
      <p style={{ fontSize:"30px" , fontWeight:"500" , marginTop:"-30px"}}>Live Data? </p>

<div style={{width:"50%" , display :"flex" ,justifyContent:"space-around" , marginTop:"20px"}} >
  <button className='btn' style={{padding:"1rem 2rem"}} >
  Yes, stop live data
  </button>
  <button className='btn' style={{padding:"1rem 2rem"}} >
  No, continue live data
  </button>
</div>
    </div>
  </div>
  )
}

export default Sure;
