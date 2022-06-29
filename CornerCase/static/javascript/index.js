window.onload=function()
{
    document.getElementById('UserFile').addEventListener('change',putContents);
    document.getElementById('EditorialFile').addEventListener('change',putContents);
    document.getElementById('GeneratorFile').addEventListener('change',putContents);
}
function putContents(event)
{ 
    var fileRead= new FileReader();
    if (this.files && this.files[0])
    {
        fileRead.readAsText(this.files[0]);
        fileRead.onload= function()
        {
            if (event.target.id=='UserFile')
            {
                document.getElementById('UserCode').innerHTML=fileRead.result;
            }
            if (event.target.id=='EditorialFile')
            {
                document.getElementById('EditorialCode').innerHTML=fileRead.result;
            }
            if (event.target.id=='GeneratorFile')
            {
                document.getElementById('GeneratorCode').innerHTML=fileRead.result;
            }
        };
        
    }
     
}