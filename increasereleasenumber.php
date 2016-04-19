#!/usr/bin/env php
<?php

if ( inreaserelease( $_SERVER["argv"][1] ) )
{
  echo "Releasenumber updated";
  exit(0);
}
exit(1);

function inreaserelease( $file )
{
 if ( file_exists( $file ))
 {
    $str = file_get_contents( $file );
	if ( preg_match_all( "/Release:\s*([0-9]{1,5})/im", $str, $matches ) )
	{
            echo "MATCH!!!";
	    $release = (int)$matches[1][0] + 1;
	    $str = preg_replace( '/(Release:\s*)([0-9]{1,5})/i', '${1}' . (string) $release, $str, 1 );
	    return file_put_contents( $file, $str );
	}
  }
}
