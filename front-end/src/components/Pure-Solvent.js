import React from 'react'

function PureSolvent({goToPage}) {
  return (
    <div className='maindiv'>
    <div style={{display:"flex" , justifyContent:"center" , alignItems:"center" ,flexDirection :"column" , height:"100%"}}>
      <p style={{ fontSize:"30px" , fontWeight:"500"}}>Is the pipetrain solvent running clean <br/>
solvent? (no biomass added)</p>
<p style={{fontSize:"22px" }}>Press when ready to start live data</p>
<div style={{width:"50%" , display :"flex" ,justifyContent:"space-around" , marginTop:"20px"}} >
  <button className='btn' style={{padding:"1rem 2rem"}} onClick={()=>goToPage(11)}>
  Yes, pure solvent now!
  </button>
  <button className='btn' style={{padding:"1rem 2rem"}} onClick={()=>goToPage(11)}>
  No, it’s not totally clean
  </button>
</div>
    </div>
  </div>
  )
}

export default PureSolvent;
