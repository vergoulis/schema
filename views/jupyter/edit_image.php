<?php
/************************************************************************************
 *
 *  Copyright (c) 2018 Thanasis Vergoulis & Konstantinos Zagganas &  Loukas Kavouras
 *  for the Information Management Systems Institute, "Athena" Research Center.
 *  
 *  This file is part of SCHeMa.
 *  
 *  SCHeMa is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *  
 *  SCHeMa is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *  
 *  You should have received a copy of the GNU General Public License
 *  along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
 *
 ************************************************************************************/
use yii\helpers\Html;
use yii\helpers\Url;
use app\components\Headers;
use yii\widgets\ActiveForm;


/*
 * Add stylesheet
 */


$this->title="Edit Jupyter image";

$cancel_icon='<i class="fas fa-times"></i>';
$save_icon='<i class="fas fa-save"></i>';

Headers::begin() ?>
<?php echo Headers::widget(
['title'=>$this->title, 
    'buttons'=>
    [

    ],
])
?>
<?php Headers::end();?>

<?php $form=ActiveForm::begin($form_params); ?>

    <?=$form->field($model,'description')?>
    <?=$form->field($model,'image')?>

    <?=Html::submitButton($save_icon . '&nbsp;Save',['class'=> 'btn btn-primary submit-btn'])?>
    <?=Html::submitButton($cancel_icon . '&nbsp;Cancel',['class'=> 'btn btn-secondary cancel-btn'])?>
<?php ActiveForm::end(); ?>

